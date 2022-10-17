import os
from typing import Any
from unittest import TestCase

from dotenv import load_dotenv
from web3 import Web3

from contract_master.polygon.contract import Erc20TokenContract

load_dotenv: Any
load_dotenv()


class TestPolycatMasterChef(TestCase):
    def test_work(self):
        contract = Erc20TokenContract(
            web3=Web3(Web3.HTTPProvider(os.getenv("QUICKNODE_POLYGON_ENDPOINT", ""))),
            address="0x49bb73b257592bb68cce4e89125482ec5263f17f",
        )
        result = contract.balance_of(account="0x283B7FAbfE6f8d41Dca3A2B63255261998bA4D13")
        print(result)
        assert isinstance(result, list)
