#!/usr/bin/env python
"""Command-line interface."""
from rich import traceback
import os.path
from os import environ
from .commands import main
from .lib import bchtracer

APPDIR = os.path.join(environ['HOME'], '.bchtracer')

BCHAPI_ENDPOINT = environ['BCHAPI_ENDPOINT'] if 'BCHAPI_ENDPOINT' in environ else 'https://api.fullstack.cash'
BCH_LEDGER_DB_FILE = environ['BCH_LEDGER_DB_FILE'] if 'BCH_LEDGER_DB_FILE' in environ else os.path.join(APPDIR, 'bch-ledger.db')

if __name__ == "__main__":
    traceback.install()
    bchtracer.config(BCHAPI_ENDPOINT=BCHAPI_ENDPOINT,
                     BCH_LEDGER_DB_FILE=BCH_LEDGER_DB_FILE)
    main(prog_name="bchtracer")  # pragma: no cover
