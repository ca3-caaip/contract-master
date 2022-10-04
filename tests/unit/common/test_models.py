from contract_master import TokenAmount


def test_is_empty():
    t1 = TokenAmount(uti="uti", symbol="symbol", decimals=8, amount="0", balance=0, original_id="id")
    t2 = TokenAmount(uti="uti", symbol="symbol", decimals=8, amount="0", balance=1, original_id="id")

    assert TokenAmount.is_empty(t1) is True
    assert TokenAmount.is_empty(t2) is False
    assert TokenAmount.is_all_empty([]) is True
    assert TokenAmount.is_all_empty([t1, t1]) is True
    assert TokenAmount.is_all_empty([t1, t2]) is False
