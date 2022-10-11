import os
from typing import Any
from unittest import TestCase

from dotenv import load_dotenv
from web3 import Web3

from contract_master.bsc.contract import NarwhalStaking

load_dotenv: Any
load_dotenv()


class TestNarwhalStaking(TestCase):
    def test_work(self):
        contract = NarwhalStaking(
            web3=Web3(Web3.HTTPProvider(os.getenv("QUICKNODE_BSC_ENDPOINT", ""))),
            address="0x6da9ee0c0571b63e38950d1e12e835d5343f601b",
            txs=[],
        )
        result = contract.balance_of(account="0x283B7FAbfE6f8d41Dca3A2B63255261998bA4D13")
        assert isinstance(result, list)
