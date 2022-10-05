from unittest import TestCase

from contract_master import (
    BalanceResult,
    CommonServiceItem,
    ErroredResult,
    GetBalanceResult,
    IgnoredResult,
    LiquidityPoolServiceItem,
    StakedServiceItem,
    TokenAmount,
    accumulate_balance_results,
)


def test_accumulate_balance_results():
    res = accumulate_balance_results(
        [
            BalanceResult(
                application="bsc",
                service="spot",
                items=[
                    CommonServiceItem(
                        type="common",
                        data=TokenAmount(
                            uti="usdt",
                            amount="0.1",
                            original_id="0x55d398326f99059ff775485246999027b3197955",
                            balance=100,
                            decimals=3,
                            symbol="USDT",
                        ),
                    )
                ],
            ),
            BalanceResult(
                application="bsc",
                service="spot",
                items=[
                    CommonServiceItem(
                        type="common",
                        data=TokenAmount(
                            uti="busd",
                            amount="0",
                            original_id="0xe9e7cea3dedca5984780bafc599bd69add087d56",
                            balance=0,
                            decimals=3,
                            symbol="BUSD",
                        ),
                    )
                ],
            ),
            BalanceResult(
                application="pancake",
                service="liquidity pool",
                items=[
                    LiquidityPoolServiceItem(
                        type="liquidity pool",
                        data=LiquidityPoolServiceItem.LiquidityPoolServiceData(
                            supply=[
                                TokenAmount(
                                    uti="cake",
                                    amount="0.3",
                                    original_id="0x0e09fabb73bd3ade0a17ecc321fd13a19e81ce82",
                                    balance=300,
                                    decimals=3,
                                    symbol="Cake",
                                ),
                                TokenAmount(
                                    uti="busd",
                                    amount="0.4",
                                    original_id="0xe9e7cea3dedca5984780bafc599bd69add087d56",
                                    balance=400,
                                    decimals=3,
                                    symbol="BUSD",
                                ),
                            ],
                            description=None,
                        ),
                    ),
                    LiquidityPoolServiceItem(
                        type="liquidity pool",
                        data=LiquidityPoolServiceItem.LiquidityPoolServiceData(
                            supply=[
                                TokenAmount(
                                    uti="cake",
                                    amount="0.5",
                                    original_id="0x0e09fabb73bd3ade0a17ecc321fd13a19e81ce82",
                                    balance=500,
                                    decimals=3,
                                    symbol="Cake",
                                ),
                                TokenAmount(
                                    uti="busd",
                                    amount="0.6",
                                    original_id="0xe9e7cea3dedca5984780bafc599bd69add087d56",
                                    balance=600,
                                    decimals=3,
                                    symbol="BUSD",
                                ),
                            ],
                            description=None,
                        ),
                    ),
                ],
            ),
            BalanceResult(
                application="pancake",
                service="staking",
                items=[
                    StakedServiceItem(
                        type="staked",
                        data=StakedServiceItem.StakedServiceData(
                            supply=[
                                TokenAmount(
                                    uti="busd",
                                    amount="0",
                                    original_id="0x0e09fabb73bd3ade0a17ecc321fd13a19e81ce82",
                                    balance=0,
                                    decimals=3,
                                    symbol="BUSD",
                                )
                            ],
                            reward=[
                                TokenAmount(
                                    uti="aog",
                                    amount="0",
                                    original_id="0x40c8225329bd3e28a043b029e0d07a5344d2c27c",
                                    balance=0,
                                    decimals=3,
                                    symbol="AOG",
                                )
                            ],
                            description=None,
                        ),
                    )
                ],
            ),
        ]
    )
    assert res == {
        "bsc": {
            "spot": [
                {
                    "type": "common",
                    "data": {
                        "uti": "usdt",
                        "amount": "0.1",
                        "original_id": "0x55d398326f99059ff775485246999027b3197955",
                        "balance": 100,
                        "decimals": 3,
                        "symbol": "USDT",
                    },
                },
            ]
        },
        "pancake": {
            "liquidity pool": [
                {
                    "type": "liquidity pool",
                    "data": {
                        "supply": [
                            {
                                "uti": "cake",
                                "amount": "0.3",
                                "original_id": "0x0e09fabb73bd3ade0a17ecc321fd13a19e81ce82",
                                "balance": 300,
                                "decimals": 3,
                                "symbol": "Cake",
                            },
                            {
                                "uti": "busd",
                                "amount": "0.4",
                                "original_id": "0xe9e7cea3dedca5984780bafc599bd69add087d56",
                                "balance": 400,
                                "decimals": 3,
                                "symbol": "BUSD",
                            },
                        ],
                        "description": None,
                    },
                },
                {
                    "type": "liquidity pool",
                    "data": {
                        "supply": [
                            {
                                "uti": "cake",
                                "amount": "0.5",
                                "original_id": "0x0e09fabb73bd3ade0a17ecc321fd13a19e81ce82",
                                "balance": 500,
                                "decimals": 3,
                                "symbol": "Cake",
                            },
                            {
                                "uti": "busd",
                                "amount": "0.6",
                                "original_id": "0xe9e7cea3dedca5984780bafc599bd69add087d56",
                                "balance": 600,
                                "decimals": 3,
                                "symbol": "BUSD",
                            },
                        ],
                        "description": None,
                    },
                },
            ],
        },
    }


class TestGetBalanceResult(TestCase):
    def test_to_json(self):
        assert (
            GetBalanceResult(
                balance_results=[
                    BalanceResult(
                        application="bsc",
                        service="spot",
                        items=[
                            CommonServiceItem(
                                type="common",
                                data=TokenAmount(
                                    uti="usdt",
                                    amount="0.1",
                                    original_id="id",
                                    balance=100,
                                    decimals=3,
                                    symbol="USDT",
                                ),
                            )
                        ],
                    )
                ],
                errored_results=[ErroredResult(address="address", reason="reason")],
                ignored_results=[IgnoredResult(address="address", reason="reason")],
            ).to_json()
            == '{"summary": {"bsc": {"spot": [{"type": "common", "data": {"uti": "usdt", "amount": "0.1",'
            ' "original_id": "id", "balance": 100, "decimals": 3, "symbol": "USDT"}}]}}, "ignored": [{"address":'
            ' "address", "reason": "reason"}], "errored": [{"address": "address", "reason": "reason"}]}'
        )
