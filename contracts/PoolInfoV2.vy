# @version 0.2.7
"""
@title Kagla Registry PoolInfo

@notice Large getters designed for off-chain use
"""

MAX_COINS: constant(int128) = 8

interface AddressProvider:
    def get_registry() -> address: view
    def admin() -> address: view

interface ZapRegistry:
    def zaps(pool: address) -> address: view

interface ERC20:
    def balanceOf(_addr: address) -> uint256: view
    def decimals() -> uint256: view
    def totalSupply() -> uint256: view
    def symbol() -> String[64]: view

interface Registry:
    def get_coins(_pool: address) -> address[MAX_COINS]: view
    def get_underlying_coins(_pool: address) -> address[MAX_COINS]: view
    def get_decimals(_pool: address) -> uint256[MAX_COINS]: view
    def get_underlying_decimals(_pool: address) -> uint256[MAX_COINS]: view
    def get_balances(_pool: address) -> uint256[MAX_COINS]: view
    def get_underlying_balances(_pool: address) -> uint256[MAX_COINS]: view
    def get_rates(_pool: address) -> uint256[MAX_COINS]: view
    def get_lp_token(_pool: address) -> address: view
    def get_parameters(_pool: address) -> PoolParams: view
    def is_meta(_pool: address) -> bool: view
    def get_pool_name(_pool: address) -> String[64]: view
    def get_pool_asset_type(_pool: address) -> uint256: view
    def get_base_pool(_pool: address) -> address: view
    def get_virtual_price_from_lp_token(_token: address) -> uint256: view

struct PoolParams:
    A: uint256
    future_A: uint256
    fee: uint256
    admin_fee: uint256
    future_fee: uint256
    future_admin_fee: uint256
    future_owner: address
    initial_A: uint256
    initial_A_time: uint256
    future_A_time: uint256

struct PoolInfo:
    balances: uint256[MAX_COINS]
    underlying_balances: uint256[MAX_COINS]
    decimals: uint256[MAX_COINS]
    underlying_decimals: uint256[MAX_COINS]
    rates: uint256[MAX_COINS]
    lp_token: address
    lp_token_total_supply: uint256
    lp_token_virtual_price: uint256
    lp_token_symbol: String[64]
    params: PoolParams
    is_meta: bool
    name: String[64]
    asset_type: uint256
    base_pool: address
    zap: address


struct PoolCoins:
    coins: address[MAX_COINS]
    underlying_coins: address[MAX_COINS]
    decimals: uint256[MAX_COINS]
    underlying_decimals: uint256[MAX_COINS]

address_provider: public(AddressProvider)
zap_registry: public(ZapRegistry)

@external
def __init__(_provider: address, _zap_registry: address):
    self.address_provider = AddressProvider(_provider)
    self.zap_registry = ZapRegistry(_zap_registry)


@view
@external
def get_pool_coins(_pool: address) -> PoolCoins:
    """
    @notice Get information on coins in a pool
    @dev Empty values in the returned arrays may be ignored
    @param _pool Pool address
    @return Coin addresses, underlying coin addresses, underlying coin decimals
    """
    registry: address = self.address_provider.get_registry()

    return PoolCoins({
        coins: Registry(registry).get_coins(_pool),
        underlying_coins: Registry(registry).get_underlying_coins(_pool),
        decimals: Registry(registry).get_decimals(_pool),
        underlying_decimals: Registry(registry).get_underlying_decimals(_pool),
    })


@view
@external
def get_pool_info(_pool: address) -> PoolInfo:
    """
    @notice Get information on a pool
    @dev Reverts if the pool address is unknown
    @param _pool Pool address
    @return balances, underlying balances, decimals, underlying decimals,
            lp token, amplification coefficient, fees
    """
    registry: address = self.address_provider.get_registry()

    lp_token: address = Registry(registry).get_lp_token(_pool)
    lp_token_total_supply: uint256 = ERC20(lp_token).totalSupply()
    lp_token_virtual_price: uint256 = 0
    if lp_token_total_supply != 0:
        lp_token_virtual_price = Registry(registry).get_virtual_price_from_lp_token(lp_token)

    return PoolInfo({
        balances: Registry(registry).get_balances(_pool),
        underlying_balances: Registry(registry).get_underlying_balances(_pool),
        decimals: Registry(registry).get_decimals(_pool),
        underlying_decimals: Registry(registry).get_underlying_decimals(_pool),
        rates: Registry(registry).get_rates(_pool),
        lp_token: lp_token,
        lp_token_total_supply: lp_token_total_supply,
        lp_token_virtual_price: lp_token_virtual_price,
        lp_token_symbol: ERC20(lp_token).symbol(),
        params: Registry(registry).get_parameters(_pool),
        is_meta: Registry(registry).is_meta(_pool),
        name: Registry(registry).get_pool_name(_pool),
        asset_type: Registry(registry).get_pool_asset_type(_pool),
        base_pool: Registry(registry).get_base_pool(_pool),
        zap: self.zap_registry.zaps(_pool)
    })
