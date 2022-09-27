from abc import ABC, abstractmethod

from pydantic.main import BaseModel
from web3 import Web3


class Balance(BaseModel):
    token: str
    balance: int
    decimals: int


class BaseContract(ABC):
    ABI: str

    def __init__(self, web3: Web3, address: str) -> None:
        self.web3: Web3 = web3
        # settlerでIDとして扱うアドレスは小文字を用いる
        self.address: str = address.lower()
        # 指定のアドレスに紐づくContractのインスタンス
        self.contract = self.web3.eth.contract(address=Web3.toChecksumAddress(address), abi=self.ABI)

    @abstractmethod
    def balance_of(self, account: str, block_height: int | None = None) -> Balance:
        pass
