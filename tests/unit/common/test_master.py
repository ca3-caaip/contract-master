from contract_master import BscContractMaster, load_master_data


def test_load_master_data():
    data = load_master_data(BscContractMaster.MASTER_CSV_FILE_PATH)
    assert len(data) > 0
