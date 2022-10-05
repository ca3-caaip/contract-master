import json
import os
from typing import Any
from unittest import TestCase

from dotenv import load_dotenv
from web3 import Web3

from contract_master import CovalentTx
from contract_master.bsc.contract import EquatorLiquidityPool

load_dotenv: Any
load_dotenv()


class TestEquatorLiquidityPool(TestCase):
    def test_work(self):
        contract = EquatorLiquidityPool(
            web3=Web3(Web3.HTTPProvider(os.getenv("QUICKNODE_BSC_ENDPOINT", ""))),
            address="0x24b1983b230b11cc3fa9ff75c73ace7cb73e1795",
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
