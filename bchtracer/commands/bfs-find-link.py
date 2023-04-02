import click
from ..lib import bchtracer
from ..lib.bchldb import LedgerQueryState
from ..lib.util import conv_legacy_address_to_cashaddr
from sys import stdout, stderr
from functools import reduce
from . import main

def bfs_find_link_sub_txs (query_engine, funding_tx, path, target_address, ignore_tx_below):
    sub_txs = []
    for txo in funding_tx['vout']:
        addr = next((a.split(':')[1] if ':' in a else a for a in txo['scriptPubKey'].get('addresses', []) if isinstance(a, str)), None)
        sub_path = path + [ { 'addr': addr, 'coin': f'''{funding_tx['hash']}:{txo['n']}''' } ]
        if target_address != addr and (ignore_tx_below < 0 or txo['value'] > ignore_tx_below):
            tx = query_engine.get_txos_spent_tx(funding_tx['hash'], txo['n'])
            if tx is not None:
                sub_txs.append({ 'tx': tx, 'path': sub_path })
    return sub_txs

def bfs_find_link_sub_matches (query_engine, funding_tx, path, target_address):
    results = []
    for txo in funding_tx['vout']:
        addr = next((a.split(':')[1] if ':' in a else a for a in txo['scriptPubKey'].get('addresses', []) if isinstance(a, str)), None)
        sub_path = path + [ { 'addr': addr, 'coin': f'''{funding_tx['hash']}:{txo['n']}''' } ]
        if target_address == addr:
            results.append(sub_path)
    return results

def bfs_find_link_sub (query_engine, guesses, target_address, ignore_tx_below, depth, max_depth, on_match_found=None):
    results = reduce(lambda a, guess: a + bfs_find_link_sub_matches(query_engine, guess['tx'], guess['path'], target_address), guesses, [])
    print(f'lvl {depth} search completed, found: {len(results)} matches', file=stderr)
    if len(results) > 0 and on_match_found is not None:
        if on_match_found(results) == True:
            return [] # when on_match_found returns True, it's a request to exit
    if depth < max_depth:
        next_lvl_guesses = reduce(lambda a, guess: a + bfs_find_link_sub_txs(query_engine, guess['tx'], guess['path'], target_address, ignore_tx_below), guesses, [])
        if len(next_lvl_guesses) > 0:
            results += bfs_find_link_sub(query_engine, next_lvl_guesses, target_address, ignore_tx_below, depth + 1, max_depth, on_match_found)
    return results

def print_txs_path (message, path, file=stdout):
    print(f'======== {message}')
    print('TXO PATH \!/')
    print(' => '.join(map(lambda a: a['coin'], path)), file=file)
    print('ADDRS PATH \!/')
    print(' => '.join(map(lambda a: a['addr'], path)), file=file)
    print('========')

@main.command('bfs-find-link')
@click.pass_context
@click.option('--funding-txo', 'funding_txo', help='The funding TXO (expected value: "txid:index").', type=str, required=True)
@click.option('--target-address', 'target_address', help='The address to lookup where the coins where spent in a chain of transactions.', type=str, required=True)
@click.option('--max-depth', help="Search's max depth.", type=int, required=True)
@click.option('--limit', help='Output limit.', type=int, default=10)
@click.option('--ignore-tx-below', 'ignore_tx_below', help='Ignore links sending less than this value.', type=float, default=-1)
def bfs_find_link (ctx, funding_txo, target_address, ignore_tx_below, limit, max_depth):
    tracer_ctx = ctx.obj
    # strip out address network
    if target_address[0] == '1':
        # convert legacy address to cashaddr
        tmp = conv_legacy_address_to_cashaddr(target_address)
        print(f'Converted target-address to cashaddr, {target_address} => {tmp}')
        target_address = tmp
    target_address = next(a.split(':')[1] if ':' in a else a for a in [target_address])
    # validate txo_txid and txo_index
    (txo_txid, txo_index) = funding_txo.split(':')
    if len(txo_txid) == 0 or not str.isnumeric(txo_index) or int(txo_index) < 0:
        raise ValueError('Expecting the funding_txo to be transaction output to be of type txid:index')
    txo_index = int(txo_index)
    chain_tip = tracer_ctx.bchldb.default_known_chain_tip
    # 30 days spaced min_blockheight_requirement, which requires updates of cached data at most in 30 days
    BLOCKHEIGHT_STEP_THRESHOLD = 144 * 30
    query_state = LedgerQueryState(
        known_chain_tip=chain_tip,
        min_blockheight_requirement=chain_tip['height'] - (chain_tip['height'] % BLOCKHEIGHT_STEP_THRESHOLD)
    )
    query_engine = tracer_ctx.bchldb.query_engine_with_state(query_state)
    funding_tx = query_engine.get_txos_spent_tx(txo_txid, txo_index)
    if funding_tx is None:
        raise ValueError('funding_txo is not spent or does not exists')
    match_len = 0
    def on_match_found (results):
        nonlocal match_len
        for index, path in enumerate(sorted(results, key=lambda a: len(a))[:limit]):
            print_txs_path(f'found path depth: {len(path)}, #{index + 1}', path)
        match_len += len(results)
        if match_len >= limit:
            return True
    results = bfs_find_link_sub(query_engine, [ { 'tx': funding_tx, 'path': [] } ], target_address, ignore_tx_below, 0, max_depth, on_match_found)
    if len(results) == 0:
        print('No path found to the target address!', file=stderr)

if __name__ == '__main__':
    bfs_find_link()
