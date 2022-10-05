import os
from typing import Any
from unittest import TestCase

from dotenv import load_dotenv
from web3 import Web3

from contract_master.bsc.contract import PumkStaking

load_dotenv: Any
load_dotenv()


class TestPumkSteaking(TestCase):
    def test_work(self):
        contract = PumkStaking(
            web3=Web3(Web3.HTTPProvider(os.getenv("QUICKNODE_BSC_ENDPOINT", ""))),
            address="0x7856a258ae3709fd5535d5f7cf7b303d1255e9e2",
            txs=[],
        )
        result = contract.balance_of(account="0x283B7FAbfE6f8d41Dca3A2B63255261998bA4D13")
        assert isinstance(result, list)
