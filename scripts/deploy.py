from brownie import ZERO_ADDRESS, AddressProvider, PoolInfo, Registry, Swaps, accounts,Contract

from scripts.add_pools import main as add_pools

# modify this prior to mainnet use
deployer = accounts.load("kagla-deploy")

ADDRESS_PROVIDER = "0x1aceb2849e249C5403Fe1331d63587ed43C78425"
GAUGE_CONTROLLER = "0xfe372d95BDFE7313435D539c87E68029A792997e"
REGISTRY = "0x91CcaC062Af9d7AC8B9Cee1Bc1A5Dc8b640758df"

def add_bai_shiden():
    registry = Registry.at(REGISTRY)
    pool = "0x4ECFc5310fD2D9A96E713E752DC1aDEBa5857D0f"
    lp_token = "0xfEbC28574b0982Baea32C2558525267bb7273F12"
    gauge = "0x9D2070D930005553D2994A202BB17C80053A4e00"
    #registry.remove_pool(pool, {"from": deployer})
    #base_pool = "0x14E8B25f260901414799A8a8662A90608Bf1fD62"
    #registry.add_metapool(pool, 2, lp_token, 18, "BAI+3KGL", base_pool, {"from": deployer})
    registry.set_liquidity_gauges("0x4ECFc5310fD2D9A96E713E752DC1aDEBa5857D0f", [gauge] + ["0x0000000000000000000000000000000000000000"] * 9, {"from": deployer})

def set_distro_address():
    provider = AddressProvider.at('0x762b149eA23070d6F021F70CB8877d2248278855', {"from": deployer})
    #distributor = Contract('0x1dA9cCB63A438F99e1a6d2b9b96794E27FBFbf12')
    distributor = '0x1dA9cCB63A438F99e1a6d2b9b96794E27FBFbf12'
    print(provider.get_address(0))
    print(provider.get_address(1))
    print(provider.get_address(2))
    print(provider.get_address(3))
    print(provider.max_id())
    ## this is dummy
    #provider.add_new_id("0x1dA9cCB63A438F99e1a6d2b9b96794E27FBFbf12", "Metapool Factory", {"from": deployer})
    #provider.add_new_id("0x1dA9cCB63A438F99e1a6d2b9b96794E27FBFbf12", "Fee Distributor", {"from": deployer})

#    provider.set_address(4, distributor, {"from": deployer})
#    print(provider.get_address(4))
    print(provider.get_address(4))


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
    add_pools_to_registry(REGISTRY)
    provider = AddressProvider.at(ADDRESS_PROVIDER)
    registry = Registry.at(REGISTRY)
    provider.set_address(0, registry, {"from": deployer})

def add_pools_to_registry(registry: REGISTRY):
    add_pools(registry, deployer)
    provider = AddressProvider.at(ADDRESS_PROVIDER)
    provider.set_address(0, registry, {"from": deployer})

def set_liquidity_gauges_shiden():
    registry = Registry.at("0x91CcaC062Af9d7AC8B9Cee1Bc1A5Dc8b640758df")
    pools = [
        "0xe5e4E9Ad8716Fe73EA440C99a92332c6328417E3", # 3pool
        "0x14E8B25f260901414799A8a8662A90608Bf1fD62", # starlay
        "0xd4CB599BD69339d020108481FA68Aec64D6D2D74" # busd        
    ]
    gauges = [
        ["0xe806e841ca26fF5A82E58A7A9144B7032623E4FB", "0x6A892edcFfafe4F64896419b1b57965e8e5bb68e"],
        ["0xc020e5D53Af59b0Fd22970f9851AcB1a12A317c6", "0x1571943e281f8C579Fcf63cBD31E425c0bFDdc74"],
        ["0x02871ff0b539E04A952e1d6cB4ae2f6eBCE7f3eD", "0xdF180f31739284a1A8Ba3a110cDdaD58642F3DAF"],
    ]
    for i in range(3):
        registry.set_liquidity_gauges(pools[i], gauges[i] + ["0x0000000000000000000000000000000000000000"] * 8, {"from": deployer})


def set_bai_shiden():
    registry = Registry.at("0x91CcaC062Af9d7AC8B9Cee1Bc1A5Dc8b640758df")
    pools = [
        "0x4ECFc5310fD2D9A96E713E752DC1aDEBa5857D0f"
    ]
    gauges = [
        ["0xe806e841ca26fF5A82E58A7A9144B7032623E4FB"],
    ]
    for i in range(1):
        registry.set_liquidity_gauges(pools[i], gauges[i] + ["0x0000000000000000000000000000000000000000"] * 9, {"from": deployer})


def set_liquidity_gauges_astar():
    registry = Registry.at("0xDA820e20A89928e43794645B9A9770057D65738B")
    pools = [
        "0xeB97BC7C4ca99Fa8078fF879905338517821B9F5", # 3pool
        "0xED29Ca5c39E35793F63f4485873ABBB52Cb29308", # starlay
        "0x247f10E06536dD774f11FA5F8309C21b6647FC9a" # busd        
    ]
    gauges = [
        ["0xa480B71b5aFBe28df9658C253e1E18A5EeDA131E", "0x35327a731cCc30C043e74E2c7385486Ef905Eb08"],
        ["0x13EE6d778B41229a8dF6a2c6EB2dcf595faFc2f4", "0x6b822dE272355524D92Ab70310035e4c573044bE"],
        ["0x940f388bb2f33C81840b70cDd72b3bC73d76232E", "0x5A2497F1C79C7a9a28224A0dBfc8e6f4EA412074"],
    ]
    for i in range(3):
        registry.set_liquidity_gauges(pools[i], gauges[i] + ["0x0000000000000000000000000000000000000000"] * 8, {"from": deployer})


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

    provider = AddressProvider.at("0x762b149eA23070d6F021F70CB8877d2248278855")

    swaps = Swaps.deploy(provider, ZERO_ADDRESS, {"from": deployer})

    if provider.max_id() == 1:
        provider.add_new_id(swaps, "Exchanges", {"from": deployer})
    else:
        provider.set_address(2, swaps, {"from": deployer})

    print(f"PoolInfo deployed to: {swaps.address}")
    print(f"Total gas used: {(balance - deployer.balance()) / 1e18:.4f} eth")


def print__():
    reg = Registry.at(REGISTRY)
    print(reg.get_pool_name('0xeB97BC7C4ca99Fa8078fF879905338517821B9F5'))
    print(reg.get_pool_name('0xED29Ca5c39E35793F63f4485873ABBB52Cb29308'))
    print(reg.get_pool_name('0x247f10E06536dD774f11FA5F8309C21b6647FC9a'))
