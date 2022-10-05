import json
from functools import reduce
from itertools import filterfalse
from typing import Any, TypeAlias

from pydantic.main import BaseModel

from .models import ServiceItem


class BalanceResult(BaseModel):
    """
    ContractMaster.get_balanceで資産取得が成功した場合の結果
    """

    application: str
    service: str
    items: list[ServiceItem]


class IgnoredResult(BaseModel):
    """
    ContractMaster.get_balanceでトークンが対象外の場合の結果
    """

    address: str
    reason: str


class ErroredResult(BaseModel):
    """
    ContractMaster.get_balanceでエラーが発生した場合の結果
    """

    address: str
    reason: str


Application: TypeAlias = str
Service: TypeAlias = str
Item: TypeAlias = dict[str, Any]
BalanceSummary = dict[Application, dict[Service, list[Item]]]


def _create_summary() -> BalanceSummary:
    return dict()


def accumulate_balance_results(balance_results: list[BalanceResult]) -> BalanceSummary:
    def combine(summary: BalanceSummary, balance: BalanceResult) -> BalanceSummary:
        additional_items = filterfalse(lambda x: x.is_empty(), balance.items)
        additional_items = list(map(lambda x: x.dict(), additional_items))
        if additional_items:
            services: dict[Service, list[Item]] = summary.get(balance.application, dict())
            existing_items: list[Item] = services.get(balance.service, list())
            services[balance.service] = existing_items + additional_items
            summary[balance.application] = services
        return summary

    return reduce(combine, balance_results, _create_summary())


class GetBalanceResult:
    """
    ContractMaster.getResult()の結果返却値
    """

    def __init__(
        self,
        balance_results: list[BalanceResult],
        ignored_results: list[IgnoredResult],
        errored_results: list[ErroredResult],
    ):
        self.balances = balance_results
        self.ignored = ignored_results
        self.errored = errored_results
        self.summary = accumulate_balance_results(balance_results)

    def to_json(self) -> str:
        return json.dumps(
            {
                "summary": self.summary,
                "ignored": list(map(lambda x: x.dict(), self.ignored)),
                "errored": list(map(lambda x: x.dict(), self.errored)),
            }
        )
