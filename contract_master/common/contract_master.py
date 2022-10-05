from abc import ABC, abstractmethod
from datetime import datetime
from typing import Literal

from .models import CovalentTx
from .result import GetBalanceResult


class ContractMaster(ABC):
    MASTER_CSV_FILE_PATH: str

    def __init__(self, txs: list[CovalentTx], user_address: str, target_datetime: datetime | None = None) -> None:
        self.user_address: str = user_address
        self.txs: list[CovalentTx] = filter_by_datetime_within(txs, target_datetime) if target_datetime else txs
        self.block_identifier: int | Literal["latest"] = get_max_block_height(txs) if target_datetime else "latest"

    @abstractmethod
    def get_balances(self) -> GetBalanceResult:
        pass


def filter_by_datetime_within(txs: list[CovalentTx], time: datetime) -> list[CovalentTx]:
    return list(filter(lambda x: x.block_signed_at <= time, txs))


def get_max_block_height(txs: list[CovalentTx]) -> int:
    if len(txs) <= 0:
        raise Exception("NoTransactionsPassed")
    return max(map(lambda x: x.block_height, txs))
