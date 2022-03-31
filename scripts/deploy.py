from brownie import ZERO_ADDRESS, AddressProvider, PoolInfo, Registry, Swaps, accounts

from scripts.add_pools import main as add_pools

# modify this prior to mainnet use
deployer = accounts.load("kagla-deploy")

ADDRESS_PROVIDER = "0x2E8de1e2911DF279644a964CdC3D1f6BaBf07a6A"
GAUGE_CONTROLLER = "0xdfA149F0e8eb9F11D3664Cf8bE867484496a4c5a"
REGISTRY = "0x0B05118f9068a0019527d78793934b52052d9025"


def coin_count():
    registry = Registry.at(REGISTRY)
    print(registry.coin_count.encode_input())
    print(registry.coin_count({"from": deployer}))


def deploy_address_provider():
    """
    Deploy `Address Provider`.
    """
    balance = deployer.balance()
    provider = AddressProvider.deploy(deployer, {"from": deployer})
    print(f"AddressProvider deployed to: {provider.address}")
    print(f"Total gas used: {(balance - deployer.balance()) / 1e18:.4f} eth")


def deploy_registry():
    """
    Deploy `Registry`, add all current pools, and set the address in `AddressProvider`.
    """
    balance = deployer.balance()
    registry = Registry.deploy(ADDRESS_PROVIDER, GAUGE_CONTROLLER, {"from": deployer})
    print(f"Registry deployed to: {registry.address}")
    print(f"Total gas used: {(balance - deployer.balance()) / 1e18:.4f} eth")

def add_pools_and_set_address():
    add_pools_to_registry()
    provider = AddressProvider.at(ADDRESS_PROVIDER)
    registry = Registry.at(REGISTRY)
    provider.set_address(0, registry, {"from": deployer})

def add_pools_to_registry():
    registry = Registry.at(REGISTRY)
    add_pools(registry, deployer)


def deploy_pool_info():
    """
    Deploy `PoolInfo` and set the address in `AddressProvider`.
    """
    balance = deployer.balance()

    provider = AddressProvider.at(ADDRESS_PROVIDER)

    pool_info = PoolInfo.deploy(provider, {"from": deployer})

    if provider.max_id() == 0:
        provider.add_new_id(pool_info, "PoolInfo Getters", {"from": deployer})
    else:
        provider.set_address(1, pool_info, {"from": deployer})

    print(f"PoolInfo deployed to: {pool_info.address}")
    print(f"Total gas used: {(balance - deployer.balance()) / 1e18:.4f} eth")


def deploy_swaps():
    """
    Deploy `Swaps` and set the address in `AddressProvider`.
    """
    balance = deployer.balance()

    provider = AddressProvider.at(ADDRESS_PROVIDER)

    swaps = Swaps.deploy(provider, ZERO_ADDRESS, {"from": deployer})

    if provider.max_id() == 1:
        provider.add_new_id(swaps, "Exchanges", {"from": deployer})
    else:
        provider.set_address(2, swaps, {"from": deployer})

    print(f"PoolInfo deployed to: {swaps.address}")
    print(f"Total gas used: {(balance - deployer.balance()) / 1e18:.4f} eth")
