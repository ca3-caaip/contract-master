from decimal import Decimal
from typing import Literal

from eth_typing.evm import ChecksumAddress
from web3 import Web3

from contract_master.common import CovalentTx, TokenAmount

from ...common import (
    Contract,
    FarmingServiceItem,
    ServiceItem,
    create_polygon_token_amount,
)
from .uni_liquidity_pool import UniLiquidityPool


class PolycatMasterChef(Contract):
    # fmt: off
    ABI = '[{"inputs":[{"internalType":"contract FishToken","name":"_fish","type":"address"},{"internalType":"uint256","name":"_startBlock","type":"uint256"},{"internalType":"address","name":"_devAddress","type":"address"},{"internalType":"address","name":"_feeAddress","type":"address"},{"internalType":"address","name":"_vaultAddress","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":true,"internalType":"uint256","name":"pid","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"Deposit","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":true,"internalType":"uint256","name":"pid","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"EmergencyWithdraw","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":true,"internalType":"address","name":"referrer","type":"address"},{"indexed":false,"internalType":"uint256","name":"commissionAmount","type":"uint256"}],"name":"ReferralCommissionPaid","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":true,"internalType":"address","name":"newAddress","type":"address"}],"name":"SetDevAddress","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":true,"internalType":"address","name":"newAddress","type":"address"}],"name":"SetFeeAddress","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":true,"internalType":"contract IReferral","name":"newAddress","type":"address"}],"name":"SetReferralAddress","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":true,"internalType":"address","name":"newAddress","type":"address"}],"name":"SetVaultAddress","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":false,"internalType":"uint256","name":"fishPerBlock","type":"uint256"}],"name":"UpdateEmissionRate","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":true,"internalType":"uint256","name":"pid","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"Withdraw","type":"event"},{"inputs":[],"name":"MAXIMUM_REFERRAL_COMMISSION_RATE","outputs":[{"internalType":"uint16","name":"","type":"uint16"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_allocPoint","type":"uint256"},{"internalType":"contract IERC20","name":"_lpToken","type":"address"},{"internalType":"uint16","name":"_depositFeeBP","type":"uint16"}],"name":"add","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_pid","type":"uint256"},{"internalType":"uint256","name":"_amount","type":"uint256"},{"internalType":"address","name":"_referrer","type":"address"}],"name":"deposit","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"devAddress","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_pid","type":"uint256"}],"name":"emergencyWithdraw","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"feeAddress","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"fish","outputs":[{"internalType":"contract FishToken","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"fishPerBlock","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_from","type":"uint256"},{"internalType":"uint256","name":"_to","type":"uint256"}],"name":"getMultiplier","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[],"name":"massUpdatePools","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_pid","type":"uint256"},{"internalType":"address","name":"_user","type":"address"}],"name":"pendingFish","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"contract IERC20","name":"","type":"address"}],"name":"poolExistence","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"poolInfo","outputs":[{"internalType":"contract IERC20","name":"lpToken","type":"address"},{"internalType":"uint256","name":"allocPoint","type":"uint256"},{"internalType":"uint256","name":"lastRewardBlock","type":"uint256"},{"internalType":"uint256","name":"accFishPerShare","type":"uint256"},{"internalType":"uint16","name":"depositFeeBP","type":"uint16"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"poolLength","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"referral","outputs":[{"internalType":"contract IReferral","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"referralCommissionRate","outputs":[{"internalType":"uint16","name":"","type":"uint16"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_pid","type":"uint256"},{"internalType":"uint256","name":"_allocPoint","type":"uint256"},{"internalType":"uint16","name":"_depositFeeBP","type":"uint16"}],"name":"set","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_devAddress","type":"address"}],"name":"setDevAddress","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_feeAddress","type":"address"}],"name":"setFeeAddress","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"contract IReferral","name":"_referral","type":"address"}],"name":"setReferralAddress","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint16","name":"_referralCommissionRate","type":"uint16"}],"name":"setReferralCommissionRate","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_vaultAddress","type":"address"}],"name":"setVaultAddress","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"startBlock","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalAllocPoint","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_fishPerBlock","type":"uint256"}],"name":"updateEmissionRate","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_pid","type":"uint256"}],"name":"updatePool","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_startBlock","type":"uint256"}],"name":"updateStartBlock","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"address","name":"","type":"address"}],"name":"userInfo","outputs":[{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"uint256","name":"rewardDebt","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"vaultAddress","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_pid","type":"uint256"},{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"withdraw","outputs":[],"stateMutability":"nonpayable","type":"function"}]'
    # fmt: on

    def __init__(self, web3: Web3, address: str, txs: list[CovalentTx]) -> None:
        super().__init__(web3, address, txs)

    def balance_of(self, account: str, block_identifier: int | Literal["latest"] = "latest") -> list[ServiceItem]:
        pids = self.__fetch_pids()
        account = Web3.toChecksumAddress(account)
        farming_service_item_list: list[ServiceItem] = []
        for pid in pids:
            rewards_token: str = self.contract.functions.fish().call(block_identifier=block_identifier)
            rewards_token_amount = self.__get_rewards_token_amount(
                pid=pid, account=account, rewards_token=rewards_token, block_identifier=block_identifier
            )
            staked_amount: int = self.contract.functions.userInfo(int(pid), account).call(
                block_identifier=block_identifier
            )[0]
            lp_token: str = self.contract.functions.poolInfo(int(pid)).call(block_identifier=block_identifier)[0]
            if lp_token != rewards_token and "lp" in self.get_symbol(lp_token).lower():
                staked_lp_info = self.__parse_staked_lp(
                    amount=staked_amount, lp_token=lp_token, block_identifier=block_identifier
                )
            else:
                staked_lp_info = [
                    create_polygon_token_amount(
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

        Contract側で"SafeMath: division by zero"のエラーを返す場合があるが、原因はtotalAllocPointで除算する箇所があるため
        このエラーはContractの利用者がいなくなった場合に発生すると思われる。エラーが発生した場合は数量0として返却する
        """
        rewards_amount: int = 0
        try:
            rewards_amount = self.contract.functions.pendingFish(int(pid), account).call(
                block_identifier=block_identifier
            )
        except Exception:
            pass

        return create_polygon_token_amount(
            token=rewards_token,
            balance=rewards_amount,
            decimals=self.get_decimals(rewards_token),
            symbol=self.get_symbol(rewards_token),
        )

    def __parse_staked_lp(
        self, amount: int, lp_token: str, block_identifier: int | Literal["latest"]
    ) -> list[TokenAmount]:
        """
        ステークしてるLP Pairから個々の量を取得して返す
        """
        lp_contract = UniLiquidityPool(web3=self.web3, address=lp_token).contract
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
            create_polygon_token_amount(
                token=token0,
                balance=user_token0_balance,
                decimals=self.get_decimals(token=token0),
                symbol=self.get_symbol(token0),
            ),
            create_polygon_token_amount(
                token=token1,
                balance=user_token1_balance,
                decimals=self.get_decimals(token1),
                symbol=self.get_symbol(token1),
            ),
        ]
