from abc import ABC, abstractmethod
from datetime import datetime
from typing import Callable

from pydantic.main import BaseModel

from .models import CovalentTx, ServiceItem
from .utils import equals, lower, unique


class BalanceResult(BaseModel):
    """
    ContractMaster.get_balanceで資産取得が成功した場合の結果
    """

    application: str
    service: str
    item: ServiceItem


class IgnoredResult(BaseModel):
    """
    ContractMaster.get_balanceでトークンが対象外の場合の結果
    """

    token: str


class ErroredResult(BaseModel):
    """
    ContractMaster.get_balanceでエラーが発生した場合の結果
    """

    token: str
    reason: str


class ContractMaster(ABC):
    MASTER_CSV_FILE_PATH: str

    def __init__(self, txs: list[CovalentTx], target_datetime: datetime, user_address: str) -> None:
        self.user_address = user_address
        self.txs = list(filter(self.__is_transaction_within(target_datetime), txs))
        self.block_height = self.__get_max_block_height(self.txs)
        fungible_token_addresses, possessable_addresses = self.__get_relevant_contract_addresses(
            base_address=user_address, transactions=self.txs
        )
        self.fungible_token_addresses = fungible_token_addresses
        self.possessable_addresses = possessable_addresses
        pass

    def __is_transaction_within(self, max_datetime: datetime) -> Callable[[CovalentTx], bool]:
        return lambda x: x.block_signed_at <= max_datetime

    def __get_max_block_height(self, transactions: list[CovalentTx]) -> int:
        if len(transactions) <= 0:
            raise Exception("NoTransactionsPassed")  # TODO: エラーハンドル
        max_block_height: int = 0
        for tx in transactions:
            if tx.block_height > max_block_height:
                max_block_height = tx.block_height
        return max_block_height

    @abstractmethod
    def get_balances(self) -> list[list[BalanceResult] | list[IgnoredResult] | list[ErroredResult]]:
        pass

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
