from contract_master.bsc.main import BscContractMaster
import argparse
import os
from dotenv import load_dotenv

load_dotenv()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--platform",
        help="--platfrom [platform]",
    )
    parser.add_argument(
        "--contract_address",
        help="--contract_address [contract_address]"
    )
    parser.add_argument(
        "--user_address",
        help="--user_address [user_address]"
    )
    parser.add_argument(
        "--block_height",
        help="--block_height [block_height]"
    )
    parser.add_argument(
        "--quicknode_endpoint",
        help="--quicknode_endpoint [quicknode_endpoint]"
    )
    args = parser.parse_args()
    if args is not None:
        if args.platform == "bsc":
            quicknode_endpoint = args.quicknode_endpoint if args.quicknode_endpoint else os.getenv("QUICKNODE_BSC_ENDPOINT")
            if quicknode_endpoint is None:
                raise Exception("No quicknode_endpoint")
            contract_master = BscContractMaster(quicknode_endpoint=quicknode_endpoint)
        else:
            raise Exception("no such platform")
        if args.user_address is not None and args.contract_address is not None:
            block_height = args.block_height if args.block_height else None
            bep20_balance = contract_master.get_bep20_token_balance(contract_address=args.contract_address, user_address=args.user_address, block_height=block_height)
            print("bep20_balance : {}".format(bep20_balance))
        elif args.user_address is None:
            raise Exception("user_address is required")
        elif args.contract_address is None:
            raise Exception("contract_address is required")
        else:
            raise Exception("unhandled args error")
    else:
        raise ValueError("There are no args")