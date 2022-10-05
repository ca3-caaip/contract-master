from typing import Literal

from eth_typing.evm import ChecksumAddress
from web3 import Web3

from contract_master.common import CovalentTx, TokenAmount

from ...common import Contract, ServiceItem, StakedServiceItem, create_bsc_token_amount


class DodoMine(Contract):
    # fmt: off
    ABI = '[{"inputs":[{"internalType":"address","name":"_dodoToken","type":"address"},{"internalType":"uint256","name":"_startBlock","type":"uint256"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"Claim","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":true,"internalType":"uint256","name":"pid","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"Deposit","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferPrepared","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":true,"internalType":"uint256","name":"pid","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"Withdraw","type":"event"},{"inputs":[],"name":"_NEW_OWNER_","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"_OWNER_","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_lpToken","type":"address"},{"internalType":"uint256","name":"_allocPoint","type":"uint256"},{"internalType":"bool","name":"_withUpdate","type":"bool"}],"name":"addLpToken","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_lpToken","type":"address"}],"name":"claim","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"claimAll","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"claimOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_lpToken","type":"address"},{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"deposit","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"dodoPerBlock","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"dodoRewardVault","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_lpToken","type":"address"}],"name":"emergencyWithdraw","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_user","type":"address"}],"name":"getAllPendingReward","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_lpToken","type":"address"}],"name":"getDlpMiningSpeed","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_lpToken","type":"address"},{"internalType":"address","name":"_user","type":"address"}],"name":"getPendingReward","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_lpToken","type":"address"}],"name":"getPid","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_user","type":"address"}],"name":"getRealizedReward","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_lpToken","type":"address"},{"internalType":"address","name":"_user","type":"address"}],"name":"getUserLpBalance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"lpTokenRegistry","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"massUpdatePools","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"poolInfos","outputs":[{"internalType":"address","name":"lpToken","type":"address"},{"internalType":"uint256","name":"allocPoint","type":"uint256"},{"internalType":"uint256","name":"lastRewardBlock","type":"uint256"},{"internalType":"uint256","name":"accDODOPerShare","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"poolLength","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"realizedReward","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_lpToken","type":"address"},{"internalType":"uint256","name":"_allocPoint","type":"uint256"},{"internalType":"bool","name":"_withUpdate","type":"bool"}],"name":"setLpToken","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_dodoPerBlock","type":"uint256"},{"internalType":"bool","name":"_withUpdate","type":"bool"}],"name":"setReward","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"startBlock","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalAllocPoint","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_pid","type":"uint256"}],"name":"updatePool","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"address","name":"","type":"address"}],"name":"userInfo","outputs":[{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"uint256","name":"rewardDebt","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_lpToken","type":"address"},{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"withdraw","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_lpToken","type":"address"}],"name":"withdrawAll","outputs":[],"stateMutability":"nonpayable","type":"function"}]'
    # fmt: on

    def __init__(self, web3: Web3, address: str, txs: list[CovalentTx]) -> None:
        super().__init__(web3, address, txs)

    def balance_of(self, account: str, block_identifier: int | Literal["latest"] = "latest") -> list[ServiceItem]:
        pids = self.__fetch_pids()
        account = Web3.toChecksumAddress(account)
        staked_service_item_list: list[ServiceItem] = []
        for pid in pids:
            rewards_token: str = "0x67ee3Cb086F8a16f34beE3ca72FAD36F7Db929e2"  # DODO Token, BSC上のDODOMINEはリワードがこれだけらしい
            staked_amount: int = self.contract.functions.userInfo(int(pid), account).call(
                block_identifier=block_identifier
            )[0]
            stake_token: str = self.contract.functions.poolInfos(int(pid)).call(block_identifier=block_identifier)[0]
            staked_token_info = self.__parse_stake_token(
                amount=staked_amount,
                stake_token=stake_token,
            )
            rewards_token_amount = self.__get_rewards_token_amount(
                account=account, rewards_token=rewards_token, stake_token=stake_token, block_identifier=block_identifier
            )
            staked_service_item_list.append(
                StakedServiceItem(
                    data=StakedServiceItem.StakedServiceData(supply=[staked_token_info], reward=[rewards_token_amount])
                )
            )
        return staked_service_item_list

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
        self, account: ChecksumAddress, rewards_token: str, stake_token: str, block_identifier: int | Literal["latest"]
    ) -> TokenAmount:
        """
        リワードを集計する
        """
        rewards_amount: int = self.contract.functions.getPendingReward(stake_token, account).call(
            block_identifier=block_identifier
        )  # BSC上のDODOMINEのリワードが１種類だけという前提でgetPendingRewardにしている。複数だった場合はgetAllPendingRewardにしてリターンもToken Amountのリストにする必要がある
        return create_bsc_token_amount(
            token=rewards_token,
            balance=rewards_amount,
            decimals=self.get_decimals(rewards_token),
            symbol=self.get_symbol(rewards_token),
        )

    def __parse_stake_token(
        self,
        amount: int,
        stake_token: str,
    ) -> TokenAmount:
        """
        ステークしてるトークンから元のトークンを識別して返す
        """

        stake_token_dict = {
            "0xBEb34A9d23E0fe41d7b08AE3A4cbAD9A63ce0aea".lower(): "0xe9e7cea3dedca5984780bafc599bd69add087d56",  # BUSD
            "0x56ce908EeBafea026ab047CEe99a3afF039B4a33".lower(): "0x55d398326f99059fF775485246999027B3197955",  # USDT
            "0xc9e1d10442296c4729270b9c1de15f742ae1c981".lower(): "0x8AC76a51cc950d9822D68b83fE1Ad97B32Cd580d",  # USDC
            "0xddee2e5f98bbe93e77f16bfa6b5669c688396f93".lower(): "0xe9e7cea3dedca5984780bafc599bd69add087d56",  # BUSD
        }
        if stake_token.lower() in stake_token_dict:
            staked = stake_token_dict[stake_token.lower()]
        else:
            print(stake_token)
            raise Exception("unknown dodo stake")

        # stake_tokenから何をステークしたかを判別できないためハードコードする
        # https://github.com/DODOEX/dodo-smart-contract/blob/master/contracts/impl/DODOLpToken.sol#L47
        # https://docs-next.vercel.app/jp/docs/1.5.0/mining
        return create_bsc_token_amount(
            token=staked,
            balance=amount,
            decimals=self.get_decimals(token=staked),
            symbol=self.get_symbol(staked),
        )
