from datetime import datetime
from os import path
from time import sleep
from typing import Type

from web3 import Web3

from contract_master.common.models import CovalentTx
from contract_master.common.utils import equals, lower, unique

from ..common import (
    BalanceResult,
    Contract,
    ContractMaster,
    ErroredResult,
    IgnoredResult,
    load_master_data,
)
from .contract import (
    Bep20TokenContract,
    CreamLendingCErc20Delegator,
    CreamLendingCEther,
    PancakeIFO,
    PancakeLiquidityPool,
    PancakeMasterChef,
    PancakeStaking,
    PancakeVault,
)


class BscContractMaster(ContractMaster):
    MASTER_CSV_FILE_PATH = path.join(path.dirname(__file__), "./master.csv")

    def __init__(self, quicknode_endpoint: str, txs: list[CovalentTx], target_datetime: datetime, user_address: str):
        super().__init__(txs, target_datetime, user_address)
        fungible_token_addresses, possessable_addresses = self.__get_relevant_contract_addresses(
            base_address=user_address, transactions=self.txs
        )
        self.fungible_token_addresses = fungible_token_addresses
        self.possessable_addresses = possessable_addresses
        self.master = load_master_data(BscContractMaster.MASTER_CSV_FILE_PATH)
        self.web3 = Web3(Web3.HTTPProvider(quicknode_endpoint))
        if not self.web3.isConnected():
            raise Exception("QuickNodeConnectionError")

    def get_balances(self) -> list[list[BalanceResult] | list[IgnoredResult] | list[ErroredResult]]:
        fungible_token_balances, fungible_errors = self.__get_fungible_token_address_balances()
        possession_balances, possesion_errors, ignored_addresses = self.__get_possessable_address_balances()
        balance_result = fungible_token_balances + possession_balances
        errors = fungible_errors + possesion_errors
        return [balance_result, errors, ignored_addresses]

    def __get_possessable_address_balances(
        self,
    ) -> tuple[list[BalanceResult], list[ErroredResult], list[IgnoredResult]]:
        possession_balances: list[BalanceResult] = list()
        errors: list[ErroredResult] = list()
        ignored_addresses: list[IgnoredResult] = list()
        for address in self.possessable_addresses:
            res = self.__get_balance(contract_address=address)
            if isinstance(res, IgnoredResult):
                ignored_addresses.append(IgnoredResult(token=address))
            elif isinstance(res, ErroredResult):
                errors.append(res)
            else:
                possession_balances.append(res)
        return (possession_balances, errors, ignored_addresses)

    def __get_fungible_token_address_balances(self) -> tuple[list[BalanceResult], list[ErroredResult]]:
        errors: list[ErroredResult] = list()
        fungible_token_balances: list[BalanceResult] = list()
        for address in self.fungible_token_addresses:
            res = self.__get_token_balance(contract_address=address)
            if isinstance(res, ErroredResult):
                errors.append(res)
            else:
                fungible_token_balances.append(res)
        return (fungible_token_balances, errors)

    def __get_token_balance(self, contract_address: str) -> BalanceResult | ErroredResult:
        sleep(0.04)  # 25回毎秒がリミットなので
        try:
            return BalanceResult(
                application="bsc",
                service="spot",
                items=Bep20TokenContract(web3=self.web3, address=contract_address).balance_of(
                    account=self.user_address, block_height=self.block_height
                ),
            )
        except Exception as e:
            return ErroredResult(token=contract_address, reason=str(e))

    def __get_balance(self, contract_address: str) -> BalanceResult | IgnoredResult | ErroredResult:
        contract: Type[Contract]
        master = self.master.get(contract_address, None)
        if master is None:
            return ErroredResult(token=contract_address, reason=f"UndefinedAddress: {contract_address}")

        match master.type:
            case "CreamLendingCEther":
                contract = CreamLendingCEther
            case "CreamLendingCErc20Delegator":
                contract = CreamLendingCErc20Delegator
            case "PancakeIFO":
                contract = PancakeIFO
            case "PancakeLiquidityPool":
                contract = PancakeLiquidityPool
            case "PancakeStaking":
                contract = PancakeStaking
            case "PancakeVault":
                contract = PancakeVault
            case "PancakeMasterChef":
                contract = PancakeMasterChef
            case "ignored":
                return IgnoredResult(token=contract_address)
            case _:
                return ErroredResult(token=contract_address, reason=f"UnsupportedType: {contract_address}")
        sleep(0.04)  # 25回毎秒がリミットなので
        try:
            return BalanceResult(
                application=master.application,
                service=master.service,
                items=contract(web3=self.web3, address=contract_address, txs=self.txs).balance_of(
                    account=self.user_address, block_height=self.block_height
                ),
            )
        except Exception as e:
            return ErroredResult(token=contract_address, reason=str(e))

    def __get_relevant_contract_addresses(
        self, base_address: str, transactions: list[CovalentTx]
    ) -> tuple[list[str], list[str]]:
        fungible_token_addresses: list[str] = []
        possessable_addresses: list[str] = []

        for tx in transactions:
            for e in tx.log_events:
                if e.decoded and e.decoded.name == "Transfer":
                    # 自分が含まれるTransferイベントのsender_addressはfungible tokenとして全て収集し、資産取得対象に含める
                    if equals(e.decoded.get_param("from"), base_address) or equals(
                        e.decoded.get_param("to"), base_address
                    ):
                        fungible_token_addresses.append(e.sender_address)
                    # 自分からどこかのコントラクトにTransferしているものはpossessableとみなし、資産取得対象に含める
                    if equals(e.decoded.get_param("from"), base_address):
                        possessable_addresses.append(e.decoded.get_param("to"))

        return unique(lower(fungible_token_addresses)), unique(lower(possessable_addresses))
