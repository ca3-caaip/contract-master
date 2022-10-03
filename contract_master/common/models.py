from datetime import datetime
from decimal import Decimal
from typing import Literal, Optional, Union

from pydantic import BaseModel

from .utils import find_first


class TokenAmount(BaseModel):
    uti: str
    amount: str
    original_id: str
    balance: int
    decimals: int
    symbol: str


class CommonServiceItem(BaseModel):
    type: Literal["common"] = "common"
    data: TokenAmount


class FarmingServiceItem(BaseModel):
    class FarmingServiceData(BaseModel):
        supply: list[TokenAmount]
        reward: list[TokenAmount]
        description: Optional[str] = None

    type: Literal["farming"] = "farming"
    data: FarmingServiceData


class StakedServiceItem(BaseModel):
    class StakedServiceData(BaseModel):
        supply: list[TokenAmount]
        reward: list[TokenAmount]
        description: Optional[str] = None

    type: Literal["staked"] = "staked"
    data: StakedServiceData


class LiquidityPoolServiceItem(BaseModel):
    class LiquidityPoolServiceData(BaseModel):
        supply: list[TokenAmount]
        description: Optional[str] = None

    type: Literal["liquidity pool"] = "liquidity pool"
    data: LiquidityPoolServiceData


class LendingServiceItem(BaseModel):
    class LendingServiceData(BaseModel):
        supply: list[TokenAmount]
        borrow: list[TokenAmount]
        reward: list[TokenAmount]
        health_rate: Optional[Decimal] = None

    type: Literal["lending"] = "lending"
    data: LendingServiceData


ServiceItem = Union[
    CommonServiceItem,
    FarmingServiceItem,
    StakedServiceItem,
    LendingServiceItem,
    LiquidityPoolServiceItem,
]


class ContractActionParams(BaseModel):
    name: str
    type: str
    indexed: bool
    value: str


class ContractAction(BaseModel):
    name: str
    signature: str
    params: list[ContractActionParams] | None

    def get_param(self, name: str) -> str:
        if self.params is None:
            raise Exception("ParamsIsNone")

        def has_same_name(target: ContractActionParams) -> bool:
            return target.name == name

        return find_first(has_same_name, self.params).value


class CovalentTxEventLog(BaseModel):
    block_signed_at: datetime
    block_height: int
    tx_offset: int
    log_offset: int
    tx_hash: str
    raw_log_topics: list[str]
    sender_contract_decimals: int | None
    sender_name: str | None  # ContractAddressの場合はContract名
    sender_contract_ticker_symbol: str | None
    sender_address: str
    sender_address_label: str | None
    sender_logo_url: str | None
    raw_log_data: str | None
    decoded: ContractAction | None

    def get_id(self) -> str:
        return f"{self.block_height}/{self.tx_offset}/{self.log_offset}"


class CovalentTx(BaseModel):
    block_signed_at: datetime
    block_height: int
    tx_hash: str
    tx_offset: int
    successful: bool
    from_address: str
    from_address_label: str | None
    to_address: str
    to_address_label: str | None
    value: str
    value_quote: str
    gas_offered: int
    gas_spent: int
    gas_price: int
    fees_paid: str | None
    gas_quote: float
    gas_quote_rate: float
    log_events: list[CovalentTxEventLog]
