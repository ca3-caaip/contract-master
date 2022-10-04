from abc import ABC, abstractmethod
from datetime import datetime
from typing import Callable

from .models import CovalentTx
from .result import GetBalanceResult


class ContractMaster(ABC):
    MASTER_CSV_FILE_PATH: str

    def __init__(self, txs: list[CovalentTx], target_datetime: datetime, user_address: str) -> None:
        self.user_address = user_address
        self.txs = list(filter(self.__is_transaction_within(target_datetime), txs))
        self.block_height = self.__get_max_block_height(self.txs)

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
    def get_balances(self) -> GetBalanceResult:
        pass
