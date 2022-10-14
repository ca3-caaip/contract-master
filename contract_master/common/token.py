from decimal import Decimal

from token_original_id.token_original_id_table import TokenOriginalIdTable

from .models import TokenAmount

token_original_id: TokenOriginalIdTable = TokenOriginalIdTable()


def create_bsc_token_amount(token: str, balance: int, decimals: int, symbol: str) -> TokenAmount:
    return TokenAmount(
        uti=str(token_original_id.get_uti(platform="bsc", token_original_id=token, default_symbol=symbol.lower())),
        amount=str(Decimal(balance) / Decimal(10**decimals)),
        original_id=token,
        balance=balance,
        decimals=decimals,
        symbol=symbol,
    )


def create_polygon_token_amount(token: str, balance: int, decimals: int, symbol: str) -> TokenAmount:
    return TokenAmount(
        uti=str(token_original_id.get_uti(platform="polygon", token_original_id=token, default_symbol=symbol.lower())),
        amount=str(Decimal(balance) / Decimal(10**decimals)),
        original_id=token,
        balance=balance,
        decimals=decimals,
        symbol=symbol,
    )
