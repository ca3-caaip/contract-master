import argparse
import json
import os
from datetime import datetime, timezone
from typing import Any

from dotenv import load_dotenv
from pydantic.main import BaseModel

from contract_master.bsc.main import BscContractMaster
from contract_master.common import CovalentTx, create_logger

load_dotenv: Any
load_dotenv()


logger = create_logger()


class Arguments(BaseModel):
    platform: str
    user_address: str
    txs_path: str
    target_datetime: datetime
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
        platform=args.platform or "bsc",
        user_address=args.user_address or "0xda28ecfc40181a6dad8b52723035dfba3386d26e",
        quicknode_endpoint=args.quicknode_endpoint or os.getenv("QUICKNODE_BSC_ENDPOINT", ""),
        target_datetime=args.target_datetime or datetime(2022, 9, 30, 1, 31, tzinfo=timezone.utc),
        txs_path=args.txs_path or os.path.join(os.path.dirname(__file__), "../sample_data/tx-0xda28ec.json"),
    )


def validate_args(args: Arguments) -> None:
    if args.platform == "bsc" and args.quicknode_endpoint is None:
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
        balances = contract_master.get_balances()
        logger.info("complete BscContractMaster.get_balances()")
        print("{}".format(balances))

    else:
        raise Exception(f"platform={args.platform} not supported")
