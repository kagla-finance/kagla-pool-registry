import json
from pathlib import Path
import os

import requests

GITHUB_POOLS = (
    "https://{}@api.github.com/repos/kagla-finance/kagla-contract/contents/contracts/pools"
)
GITHUB_POOLDATA = "https://{}@raw.githubusercontent.com/kagla-finance/kagla-contract/main/contracts/pools/{}/pooldata.json"  # noqa: E501


def get_pool_data(force_fetch: bool = False) -> dict:
    """
    Fetch data about existing Kagla pools from Github.

    Pool Data is pulled from `kagla-contract/contacts/pools/[POOL_NAME]/pooldata.json`
    and stored at `./pooldata.json`. This JSON is then used for adding new pools to the registry
    and for forked-mainnet testing.

    To update the pools, delete `pooldata.json` or use `brownie run get_pool_data`
    """
    token = os.environ["GITHUB_TOKEN"]
    path = Path(__file__).parent.parent.joinpath("pooldata.json")

    if not force_fetch and path.exists():
        try:
            with path.open() as fp:
                return json.load(fp)
        except (json.JSONDecodeError, FileNotFoundError):
            pass

    print("Querying Github for pool deployments...")
    pool_data = {}
    pool_names = [
        i["name"] for i in requests.get(GITHUB_POOLS.format(token)).json() if i["type"] == "dir"
    ]

    for name in pool_names:
        data = requests.get(GITHUB_POOLDATA.format(token, name)).json()
        if "swap_address" not in data:
            print(f"Cannot add {name} - no deployment address!")
            continue
        pool_data[name] = data

    with path.open("w") as fp:
        json.dump(pool_data, fp, sort_keys=True, indent=2)

    print(f"Pool deployment data saved at {path.as_posix()}")
    return pool_data


def main():
    return get_pool_data(True)
