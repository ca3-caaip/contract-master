import os
from typing import Any
from unittest import TestCase

from dotenv import load_dotenv
from web3 import Web3

from contract_master import LendingServiceItem
from contract_master.bsc.contract import CreamLendingCEther

load_dotenv: Any
load_dotenv()


class TestCreamLendingCEther(TestCase):
    def test_work(self):
        contract = CreamLendingCEther(
            web3=Web3(Web3.HTTPProvider(os.getenv("QUICKNODE_BSC_ENDPOINT", ""))),
            address="0x1ffe17b99b439be0afc831239ddecda2a790ff3a",
            txs=[],
        )
        result = contract.balance_of(account="0x283B7FAbfE6f8d41Dca3A2B63255261998bA4D13")
        assert isinstance(result, LendingServiceItem)
