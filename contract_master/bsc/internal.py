import csv
from os import path

from pydantic import BaseModel


class MasterData(BaseModel):
    address: str
    type: str
    name: str


def load_master_data() -> dict[str, MasterData]:
    with open(path.join(path.dirname(__file__), "./master.csv"), "r", newline="") as csvfile:
        data = csv.DictReader(csvfile)
        data = map(MasterData.parse_obj, data)
        data = map(lambda x: (x.address, x), data)
        return dict(list(data))
