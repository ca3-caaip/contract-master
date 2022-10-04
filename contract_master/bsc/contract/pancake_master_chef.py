from decimal import Decimal
from typing import Literal

from eth_typing.evm import ChecksumAddress
from web3 import Web3

from contract_master.common import CovalentTx, TokenAmount

from ...common import Contract, FarmingServiceItem, ServiceItem, create_bsc_token_amount
from .pancake_liquidity_pool import PancakeLiquidityPool


class PancakeMasterChef(Contract):
    # fmt: off
    ABI = '[{"inputs":[{"internalType":"contract CakeToken","name":"_cake","type":"address"},{"internalType":"contract SyrupBar","name":"_syrup","type":"address"},{"internalType":"address","name":"_devaddr","type":"address"},{"internalType":"uint256","name":"_cakePerBlock","type":"uint256"},{"internalType":"uint256","name":"_startBlock","type":"uint256"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":true,"internalType":"uint256","name":"pid","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"Deposit","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":true,"internalType":"uint256","name":"pid","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"EmergencyWithdraw","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":true,"internalType":"uint256","name":"pid","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"Withdraw","type":"event"},{"inputs":[],"name":"BONUS_MULTIPLIER","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_allocPoint","type":"uint256"},{"internalType":"contract IBEP20","name":"_lpToken","type":"address"},{"internalType":"bool","name":"_withUpdate","type":"bool"}],"name":"add","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"cake","outputs":[{"internalType":"contract CakeToken","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"cakePerBlock","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_pid","type":"uint256"},{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"deposit","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_devaddr","type":"address"}],"name":"dev","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"devaddr","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_pid","type":"uint256"}],"name":"emergencyWithdraw","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"enterStaking","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_from","type":"uint256"},{"internalType":"uint256","name":"_to","type":"uint256"}],"name":"getMultiplier","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"leaveStaking","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"massUpdatePools","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_pid","type":"uint256"}],"name":"migrate","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"migrator","outputs":[{"internalType":"contract IMigratorChef","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_pid","type":"uint256"},{"internalType":"address","name":"_user","type":"address"}],"name":"pendingCake","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"poolInfo","outputs":[{"internalType":"contract IBEP20","name":"lpToken","type":"address"},{"internalType":"uint256","name":"allocPoint","type":"uint256"},{"internalType":"uint256","name":"lastRewardBlock","type":"uint256"},{"internalType":"uint256","name":"accCakePerShare","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"poolLength","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_pid","type":"uint256"},{"internalType":"uint256","name":"_allocPoint","type":"uint256"},{"internalType":"bool","name":"_withUpdate","type":"bool"}],"name":"set","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"contract IMigratorChef","name":"_migrator","type":"address"}],"name":"setMigrator","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"startBlock","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"syrup","outputs":[{"internalType":"contract SyrupBar","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalAllocPoint","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"multiplierNumber","type":"uint256"}],"name":"updateMultiplier","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_pid","type":"uint256"}],"name":"updatePool","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"address","name":"","type":"address"}],"name":"userInfo","outputs":[{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"uint256","name":"rewardDebt","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_pid","type":"uint256"},{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"withdraw","outputs":[],"stateMutability":"nonpayable","type":"function"}]'
    # fmt: on

    def __init__(self, web3: Web3, address: str, txs: list[CovalentTx]) -> None:
        super().__init__(web3, address, txs)

    def balance_of(self, account: str, block_height: int | None = None) -> list[ServiceItem]:
        pids = self.__fetch_pids()
        account = Web3.toChecksumAddress(account)
        block_identifier = block_height if block_height else "latest"
        farming_service_item_list: list[ServiceItem] = []
        for pid in pids:
            rewards_token: str = self.contract.functions.cake().call(block_identifier=block_identifier)
            rewards_token_amount = self.__get_rewards_token_amount(
                pid=pid, account=account, rewards_token=rewards_token, block_identifier=block_identifier
            )
            staked_amount: int = self.contract.functions.userInfo(int(pid), account).call(
                block_identifier=block_identifier
            )[0]
            lp_token: str = self.contract.functions.poolInfo(int(pid)).call(block_identifier=block_identifier)[0]
            if lp_token != rewards_token:
                staked_lp_info = self.__parse_staked_lp(
                    amount=staked_amount, lp_token=lp_token, block_identifier=block_identifier
                )
            else:
                staked_lp_info = [
                    create_bsc_token_amount(
                        token=lp_token,
                        balance=staked_amount,
                        decimals=self.get_decimals(lp_token),
                        symbol=self.get_symbol(lp_token),
                    )
                ]
            farming_service_item = FarmingServiceItem(
                data=FarmingServiceItem.FarmingServiceData(reward=[rewards_token_amount], supply=staked_lp_info)
            )
            farming_service_item_list.append(farming_service_item)
        return farming_service_item_list

    def __fetch_pids(self) -> list[str]:
        """
        ステーキングされているものを取得するのに必要なPIDをトランザクションから探している。PIDの数が最終的なリストの長さになる
        """
        txs = self.txs
        if txs is None:
            raise ValueError("There are no Transactions")
        pids: list[str] = []
        for tx in txs:
            for e in tx.log_events:
                if e.sender_address == self.address and e.decoded and e.decoded.name == "Deposit":
                    if e.decoded.get_param("pid"):
                        pid = e.decoded.get_param("pid")
                        if pid not in pids:
                            pids.append(pid)
        return pids

    def __get_rewards_token_amount(
        self, pid: str, account: ChecksumAddress, rewards_token: str, block_identifier: int | Literal["latest"]
    ) -> TokenAmount:
        """
        リワードを集計する
        """
        rewards_amount: int = self.contract.functions.pendingCake(int(pid), account).call(
            block_identifier=block_identifier
        )
        return create_bsc_token_amount(
            token=rewards_token,
            balance=rewards_amount,
            decimals=self.get_decimals(rewards_token),
            symbol=self.get_symbol(rewards_token),
        )

    def __parse_staked_lp(
        self, amount: int, lp_token: str, block_identifier: int | Literal["latest"]
    ) -> list[TokenAmount]:
        """
        ステークしてるLP Pairからここの量を取得して返す
        """
        lp_contract = PancakeLiquidityPool(web3=self.web3, address=lp_token).contract
        token0: str = lp_contract.functions.token0().call(block_identifier=block_identifier)
        token1: str = lp_contract.functions.token1().call(block_identifier=block_identifier)
        reserves: list[int] = lp_contract.functions.getReserves().call(block_identifier=block_identifier)
        token0_reserve: int = reserves[0]
        token1_reserve: int = reserves[1]
        total_supply: int = lp_contract.functions.totalSupply().call(block_identifier=block_identifier)
        user_share: Decimal = Decimal(amount) / Decimal(total_supply)
        user_token0_balance = int(token0_reserve * user_share)
        user_token1_balance = int(token1_reserve * user_share)

        return [
            create_bsc_token_amount(
                token=token0,
                balance=user_token0_balance,
                decimals=self.get_decimals(token=token0),
                symbol=self.get_symbol(token0),
            ),
            create_bsc_token_amount(
                token=token1,
                balance=user_token1_balance,
                decimals=self.get_decimals(token1),
                symbol=self.get_symbol(token1),
            ),
        ]
