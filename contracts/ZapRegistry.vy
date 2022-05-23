# @version 0.2.11
"""
@title Kagla Zap Registry

"""

interface AddressProvider:
    def admin() -> address: view

event ZapAdded:
    pool: address
    zap: address

address_provider: public(AddressProvider)
zaps: public(HashMap[address, address])
@external
def __init__(_address_provider: address):
    """
    @notice Constructor function
    """
    self.address_provider = AddressProvider(_address_provider)

@external
def add_zap(pool: address, zap: address): 
    assert msg.sender == self.address_provider.admin()  # dev: admin-only function
    self.zaps[pool] = zap
    log ZapAdded(pool, zap)
