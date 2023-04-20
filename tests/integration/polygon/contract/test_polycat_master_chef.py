import json
import os
from typing import Any
from unittest import TestCase

from dotenv import load_dotenv
from web3 import Web3

from contract_master.common import CovalentTx
from contract_master.polygon.contract import PolycatMasterChef

load_dotenv: Any
load_dotenv()


def open_tx_files(path: str) -> list[CovalentTx]:
    with open(path, "r") as f:
        txs = json.load(f)
    txs = list(map(lambda x: CovalentTx.parse_obj(x), txs))
    return txs


class TestPolycatMasterChef(TestCase):
    def test_work(self):
        contract = PolycatMasterChef(
            web3=Web3(Web3.HTTPProvider(os.getenv("QUICKNODE_POLYGON_ENDPOINT", ""))),
            address="0x8cfd1b9b7478e7b0422916b72d1db6a9d513d734",
            txs=open_tx_files(path="sample_data/polygon/tx-0x283b7f.json"),
        )
        result = contract.balance_of(
            account="0x283B7FAbfE6f8d41Dca3A2B63255261998bA4D13"
        )
        print(result)
        assert isinstance(result, list)
