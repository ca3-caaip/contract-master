import os
from typing import Any
from unittest import TestCase

from dotenv import load_dotenv
from web3 import Web3

from contract_master.bsc.contract import PumkBnbStaking

load_dotenv: Any
load_dotenv()


class TestPumkBnbSteaking(TestCase):
    def test_work(self):
        contract = PumkBnbStaking(
            web3=Web3(Web3.HTTPProvider(os.getenv("QUICKNODE_BSC_ENDPOINT", ""))),
            address="0x28549206edf0ae5f63e14020de58e05da540c4c4",
            txs=[],
        )
        result = contract.balance_of(account="0x283B7FAbfE6f8d41Dca3A2B63255261998bA4D13")
        assert isinstance(result, list)
