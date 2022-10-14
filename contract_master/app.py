import argparse
import json
import os
from datetime import datetime
from typing import Any

from dotenv import load_dotenv
from pydantic.main import BaseModel

from contract_master.bsc.main import BscContractMaster
from contract_master.common import CovalentTx, create_logger
from contract_master.polygon.main import PolygonContractMaster

load_dotenv: Any
load_dotenv()


logger = create_logger()


class Arguments(BaseModel):
    platform: str
    user_address: str
    txs_path: str
    target_datetime: datetime | None
    quicknode_endpoint: str


def open_tx_files(path: str) -> list[CovalentTx]:
    with open(path, "r") as f:
        txs = json.load(f)
    txs = list(map(lambda x: CovalentTx.parse_obj(x), txs))
    return txs


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--platform",
        help="--platfrom [platform]",
    )
    parser.add_argument("--user_address", help="--user_address [user_address]")
    parser.add_argument("--quicknode_endpoint", help="--quicknode_endpoint [quicknode_endpoint]")
    parser.add_argument("--target_datetime", help="--target_datetime [target_datetime]")
    parser.add_argument("--txs_path", help="--txs_path [txs_path]")
    args = parser.parse_args()

    return Arguments(
        platform=args.platform or "polygon",
        user_address=args.user_address or "0x283B7FAbfE6f8d41Dca3A2B63255261998bA4D13",
        quicknode_endpoint=args.quicknode_endpoint or os.getenv("QUICKNODE_POLYGON_ENDPOINT", ""),
        target_datetime=args.target_datetime or None,  # e.g. datetime(2022, 9, 30, 1, 31, tzinfo=timezone.utc)
        txs_path=args.txs_path or os.path.join(os.path.dirname(__file__), "../sample_data/polygon/tx-0x283b7f.json"),
    )


def validate_args(args: Arguments) -> None:
    if args.platform == "bsc" and args.quicknode_endpoint is None:
        raise Exception("No quicknode_endpoint")
    if args.platform == "polygon" and args.quicknode_endpoint is None:
        raise Exception("No quicknode_endpoint")


if __name__ == "__main__":
    logger.info("app start")
    args = parse_args()
    validate_args(args)

    if args.platform == "bsc":
        logger.info(f"initialize BscContractMaster with loading transactions from {args.txs_path}")
        contract_master = BscContractMaster(
            txs=open_tx_files(args.txs_path),
            quicknode_endpoint=args.quicknode_endpoint,
            target_datetime=args.target_datetime,
            user_address=args.user_address,
        )
        logger.info("start to BscContractMaster.get_balances()")
        result = contract_master.get_balances()
        logger.info("complete BscContractMaster.get_balances()")
        print(result.to_json())

    if args.platform == "polygon":
        logger.info(f"initialize PolygonContractMaster with loading transactions from {args.txs_path}")
        contract_master = PolygonContractMaster(
            txs=open_tx_files(args.txs_path),
            quicknode_endpoint=args.quicknode_endpoint,
            target_datetime=args.target_datetime,
            user_address=args.user_address,
        )
        logger.info("start to PolygonContractMaster.get_balances()")
        result = contract_master.get_balances()
        logger.info("complete PolygonContractMaster.get_balances()")
        print(result.to_json())
    else:
        raise Exception(f"platform={args.platform} not supported")
