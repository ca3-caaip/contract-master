from web3 import Web3

from .internal import load_abi, load_master_data


class BscContractMaster:
    def __init__(self, quicknode_endpoint: str):
        self.master = load_master_data()
        self.web3 = Web3(Web3.HTTPProvider(quicknode_endpoint))
        if not self.web3.isConnected():
            raise Exception("QuickNodeConnectionError")

    def balance_of(self, contract_address: str, user_address: str, block_height: int | None = None) -> dict[str, str]:
        contract_address = contract_address.lower()
        user_address = Web3.toChecksumAddress(user_address)
        block_identifier = block_height if block_height else "latest"

        contract = self.get_contract(contract_address)
        balance = contract.functions.balanceOf(user_address).call(block_identifier=block_identifier)
        return {contract_address: balance}

    def get_balance(self, contract_address: str, user_address: str, block_height: int | None = None) -> dict[str, str]:
        contract_address = contract_address.lower()
        user_address = Web3.toChecksumAddress(user_address)
        block_identifier = block_height if block_height else "latest"
        master = self.master[contract_address]

        match master.type:
            case "bep20":
                contract = self.get_contract(contract_address)
                balance = contract.functions.balanceOf(user_address).call(block_identifier=block_identifier)
                return {contract_address: balance}

            case _:
                raise Exception("AddressNotSupported")

    def get_contract(self, address: str):
        return self.web3.eth.contract(address=Web3.toChecksumAddress(address), abi=load_abi(self.master[address].type))
