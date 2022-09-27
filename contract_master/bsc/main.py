from web3 import Web3

from .contract import Balance, Bep20TokenContract
from .internal import load_master_data


class BscContractMaster:
    def __init__(self, quicknode_endpoint: str):
        self.master = load_master_data()
        self.web3 = Web3(Web3.HTTPProvider(quicknode_endpoint))
        if not self.web3.isConnected():
            raise Exception("QuickNodeConnectionError")

    def get_bep20_token_balance(
        self, contract_address: str, user_address: str, block_height: int | None = None
    ) -> Balance:
        return Bep20TokenContract(web3=self.web3, address=contract_address).balance_of(
            account=user_address, block_height=block_height
        )

    def get_balance(self, contract_address: str, user_address: str, block_height: int | None = None) -> list[Balance]:
        master = self.master[contract_address]

        match master.type:
            case _:
                raise Exception("AddressNotSupported")
