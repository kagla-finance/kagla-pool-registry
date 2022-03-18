from email.headerregistry import Address
from brownie import ZERO_ADDRESS, AddressProvider, PoolInfo, Registry, Swaps, accounts

from scripts.add_pools import main as add_pools

# modify this prior to mainnet use
deployer = accounts.load("kagla-deploy")

ADDRESS_PROVIDER = "0x5067bF2952D3F3c184f3dc707F8CF6Dc4eab5858"
GAUGE_CONTROLLER = "0x060DE8b98b5B1Cd9b387632099AC3b6B3308A822"
REGISTRY = "0xf4A3D2215A39D1a2090eDd787ACb705bacA914D0"


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

    provider = AddressProvider.at(ADDRESS_PROVIDER)
    registry = Registry.deploy(
        ADDRESS_PROVIDER, GAUGE_CONTROLLER, {"from": deployer}
    )
    add_pools(registry, deployer)
    provider.set_address(0, registry, {"from": deployer})

    print(f"Registry deployed to: {registry.address}")
    print(f"Total gas used: {(balance - deployer.balance()) / 1e18:.4f} eth")


def deploy_pool_info():
    """
    Deploy `PoolInfo` and set the address in `AddressProvider`.
    """
    balance = deployer.balance()

    provider = AddressProvider.at(ADDRESS_PROVIDER)

    pool_info = PoolInfo.deploy(provider, {"from": deployer})

    if provider.max_id() == 0:
        provider.add_new_id(
            pool_info, "PoolInfo Getters", {"from": deployer}
        )
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
