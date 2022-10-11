from datetime import datetime
from os import path
from time import sleep
from typing import Type

from web3 import Web3

from ..common import (
    BalanceResult,
    Contract,
    ContractMaster,
    CovalentTx,
    ErroredResult,
    GetBalanceResult,
    IgnoredResult,
    equals,
    load_master_data,
    lower,
    unique,
)
from .contract import (
    Bep20TokenContract,
    CreamLendingCErc20Delegator,
    CreamLendingCEther,
    DodoMine,
    EquatorLiquidityPool,
    NarwhalStaking,
    PancakeIFO,
    PancakeLiquidityPool,
    PancakeMasterChef,
    PancakeStaking,
    PancakeVault,
    PumkBnbStaking,
    PumkStaking,
    StablexSuperChef,
)


class BscContractMaster(ContractMaster):
    MASTER_CSV_FILE_PATH = path.join(path.dirname(__file__), "./master.csv")

    def __init__(
        self, quicknode_endpoint: str, txs: list[CovalentTx], user_address: str, target_datetime: datetime | None = None
    ):
        super().__init__(txs, user_address, target_datetime)
        eoa_addresses, fungible_token_addresses, possessable_addresses = self.__get_relevant_contract_addresses(
            base_address=user_address, transactions=self.txs
        )
        self.eoa_addresses = eoa_addresses
        self.fungible_token_addresses = fungible_token_addresses
        self.possessable_addresses = possessable_addresses
        self.master = load_master_data(BscContractMaster.MASTER_CSV_FILE_PATH)
        self.web3 = Web3(Web3.HTTPProvider(quicknode_endpoint))
        if not self.web3.isConnected():
            raise Exception("QuickNodeConnectionError")
        self.web3.eth.default_block = self.block_identifier

    def get_balances(self) -> GetBalanceResult:
        fungible_token_balances, fungible_errors = self.__get_fungible_token_balances()
        possessable_balances, possessable_errors, possessable_ignored = self.__get_possessable_address_balances()
        return GetBalanceResult(
            balance_results=fungible_token_balances + possessable_balances,
            ignored_results=possessable_ignored,
            errored_results=fungible_errors + possessable_errors,
        )

    def __get_possessable_address_balances(
        self,
    ) -> tuple[list[BalanceResult], list[ErroredResult], list[IgnoredResult]]:
        balances: list[BalanceResult] = list()
        errored: list[ErroredResult] = list()
        ignored: list[IgnoredResult] = list()
        for address in self.possessable_addresses:
            res = self.__get_balance(address=address)
            sleep(0.04)  # 25回毎秒がリミットなので
            if isinstance(res, IgnoredResult):
                ignored.append(res)
            elif isinstance(res, ErroredResult):
                errored.append(res)
            else:
                balances.append(res)
        return balances, errored, ignored

    def __get_fungible_token_balances(self) -> tuple[list[BalanceResult], list[ErroredResult]]:
        errors: list[ErroredResult] = list()
        fungible_token_balances: list[BalanceResult] = list()
        for address in self.fungible_token_addresses:
            res = self.__get_token_balance(contract_address=address)
            sleep(0.04)  # 25回毎秒がリミットなので
            if isinstance(res, ErroredResult):
                errors.append(res)
            else:
                fungible_token_balances.append(res)
        return fungible_token_balances, errors

    def __get_token_balance(self, contract_address: str) -> BalanceResult | ErroredResult:
        try:
            return BalanceResult(
                application="bsc",
                service="spot",
                items=Bep20TokenContract(web3=self.web3, address=contract_address).balance_of(
                    account=self.user_address, block_identifier=self.block_identifier
                ),
            )
        except Exception as e:
            return ErroredResult(address=contract_address, reason=str(e))

    def __get_balance(self, address: str) -> BalanceResult | IgnoredResult | ErroredResult:
        contract: Type[Contract]
        master = self.master.get(address, None)
        if master is None:
            if self.__is_contract(address):
                return ErroredResult(address=address, reason="MasterNotDefined")
            else:
                return IgnoredResult(address=address, reason="EOA")

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
            case "DodoMine":
                contract = DodoMine
            case "StablexSuperChef":
                contract = StablexSuperChef
            case "EquatorLiquidityPool":
                contract = EquatorLiquidityPool
            case "PumkStaking":
                contract = PumkStaking
            case "PumkBnbStaking":
                contract = PumkBnbStaking
            case "NarwhalStaking":
                contract = NarwhalStaking
            case "ignored":
                return IgnoredResult(address=address, reason="IgnoreType")
            case _:
                return ErroredResult(address=address, reason="NotImplemented")
        try:
            return BalanceResult(
                application=master.application,
                service=master.service,
                items=contract(web3=self.web3, address=address, txs=self.txs).balance_of(
                    account=self.user_address, block_identifier=self.block_identifier
                ),
            )
        except Exception as e:
            return ErroredResult(address=address, reason=str(e))

    def __get_relevant_contract_addresses(
        self, base_address: str, transactions: list[CovalentTx]
    ) -> tuple[list[str], list[str], list[str]]:
        eoa_addresses: list[str] = []
        fungible_token_addresses: list[str] = []
        possessable_addresses: list[str] = []

        for tx in transactions:
            # Transactionのfromは必ずEOA
            eoa_addresses.append(tx.from_address)

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

        return (
            unique(lower(eoa_addresses)),
            unique(lower(fungible_token_addresses)),
            unique(lower(possessable_addresses)),
        )

    def __is_contract(self, address: str) -> bool:
        return self.web3.eth.get_code(Web3.toChecksumAddress(address)) != b""
