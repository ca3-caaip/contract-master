from datetime import datetime
from typing import Any

from pydantic.main import BaseModel

from contract_master import filter_by_datetime_within, get_max_block_height


def test_filter_by_datetime_within():
    class TestData(BaseModel):
        block_signed_at: datetime

    test_data: list[Any] = [
        TestData(block_signed_at=datetime.fromisoformat("2022-10-05")),
        TestData(block_signed_at=datetime.fromisoformat("2022-10-06")),
        TestData(block_signed_at=datetime.fromisoformat("2022-10-07")),
    ]
    expected: list[Any] = [
        TestData(block_signed_at=datetime.fromisoformat("2022-10-05")),
        TestData(block_signed_at=datetime.fromisoformat("2022-10-06")),
    ]

    assert filter_by_datetime_within(test_data, datetime.fromisoformat("2022-10-06")) == expected


def test_get_max_block_height():
    class TestData(BaseModel):
        block_height: int

    test_data: list[Any] = [
        TestData(block_height=1),
        TestData(block_height=2),
        TestData(block_height=3),
    ]

    assert get_max_block_height(test_data) == 3
