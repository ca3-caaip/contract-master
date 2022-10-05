import json
import os
from typing import Any
from unittest import TestCase

from dotenv import load_dotenv
from web3 import Web3

from contract_master import CovalentTx
from contract_master.bsc.contract import DodoMine

load_dotenv: Any
load_dotenv()


class TestDodoMine(TestCase):
    def test_work(self):
        contract = DodoMine(
            web3=Web3(Web3.HTTPProvider(os.getenv("QUICKNODE_BSC_ENDPOINT", ""))),
            address="0x01f9bfac04e6184e90bd7eafd51999ce430cc750",
            txs=self.open_tx_files("sample_data/tx-0x283b7f.json"),
        )
        result = contract.balance_of(account="0x283B7FAbfE6f8d41Dca3A2B63255261998bA4D13")
        print(result)
        assert isinstance(result, list)

    def open_tx_files(self, path: str) -> list[CovalentTx]:
        with open(path, "r") as f:
            txs = json.load(f)
        txs = list(map(lambda x: CovalentTx.parse_obj(x), txs))
        return txs
