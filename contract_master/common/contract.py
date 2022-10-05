from abc import ABC, abstractmethod
from typing import Literal

from web3 import Web3

from .models import CovalentTx, ServiceItem


class Contract(ABC):
    ABI: str
    BEP20_ABI: str = '[{"constant":true,"inputs":[],"name":"name","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"guy","type":"address"},{"name":"wad","type":"uint256"}],"name":"approve","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"src","type":"address"},{"name":"dst","type":"address"},{"name":"wad","type":"uint256"}],"name":"transferFrom","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"wad","type":"uint256"}],"name":"withdraw","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"","type":"address"}],"name":"balanceOf","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"dst","type":"address"},{"name":"wad","type":"uint256"}],"name":"transfer","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[],"name":"deposit","outputs":[],"payable":true,"stateMutability":"payable","type":"function"},{"constant":true,"inputs":[{"name":"","type":"address"},{"name":"","type":"address"}],"name":"allowance","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"payable":true,"stateMutability":"payable","type":"fallback"},{"anonymous":false,"inputs":[{"indexed":true,"name":"src","type":"address"},{"indexed":true,"name":"guy","type":"address"},{"indexed":false,"name":"wad","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"src","type":"address"},{"indexed":true,"name":"dst","type":"address"},{"indexed":false,"name":"wad","type":"uint256"}],"name":"Transfer","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"dst","type":"address"},{"indexed":false,"name":"wad","type":"uint256"}],"name":"Deposit","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"src","type":"address"},{"indexed":false,"name":"wad","type":"uint256"}],"name":"Withdrawal","type":"event"}]'

    def __init__(self, web3: Web3, address: str, txs: list[CovalentTx] | None = None) -> None:
        self.web3: Web3 = web3
        # settlerでIDとして扱うアドレスは小文字を用いる
        self.address: str = address.lower()
        # 指定のアドレスに紐づくContractのインスタンス
        self.contract = self.web3.eth.contract(address=Web3.toChecksumAddress(address), abi=self.ABI)
        self.txs = txs

    @abstractmethod
    def balance_of(self, account: str, block_identifier: int | Literal["latest"] = "latest") -> list[ServiceItem]:
        pass

    def get_symbol(self, token: str) -> str:
        """
        対象tokenのsymbolを取得する
        symbolメソッドはBEP20標準規格
        """
        return (
            self.web3.eth.contract(address=Web3.toChecksumAddress(token), abi=self.BEP20_ABI).functions.symbol().call()
        )

    def get_decimals(self, token: str) -> int:
        """
        対象tokenのdecimalsを取得する
        decimalsメソッドはBEP20標準規格
        """
        return (
            self.web3.eth.contract(address=Web3.toChecksumAddress(token), abi=self.BEP20_ABI)
            .functions.decimals()
            .call()
        )
