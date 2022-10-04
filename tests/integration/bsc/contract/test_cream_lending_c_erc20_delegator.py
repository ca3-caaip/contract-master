import os
from typing import Any
from unittest import TestCase

from dotenv import load_dotenv
from web3 import Web3

from contract_master import LendingServiceItem
from contract_master.bsc.contract import CreamLendingCErc20Delegator

load_dotenv: Any
load_dotenv()


class TestCreamLendingCErc20Delegator(TestCase):
    def test_work(self):
        contract = CreamLendingCErc20Delegator(
            web3=Web3(Web3.HTTPProvider(os.getenv("QUICKNODE_BSC_ENDPOINT", ""))),
            address="0xd83c88db3a6ca4a32fff1603b0f7ddce01f5f727",
            txs=[],
        )
        result = contract.balance_of(account="0x283B7FAbfE6f8d41Dca3A2B63255261998bA4D13")
        assert isinstance(result, LendingServiceItem)
