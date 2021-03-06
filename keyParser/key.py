from platon.packages.platon_keys.datatypes import PrivateKey
from platon.packages.platon_keys.utils import address as Address


def private_key_to_address(private_key: str, prefix=None):
    """
    Args:
        private_key: private key hex string
        prefix: expected bech32 address prefix, if none, return hex address
    """
    pk_bytes = bytes.fromhex(private_key)
    Private_Key = PrivateKey(pk_bytes)
    address = Private_Key.public_key.to_address()
    if not prefix:
        return address
    return hex_address_to_bech32_address(address[2:], prefix)


def hex_address_to_bech32_address(address: str, prefix: str):
    """
    Args:
        address: hex address string
        prefix: expected bech32 address prefix
    """
    hex_address = bytes.fromhex(address)
    return Address.address_bytes_to_bech32_address(hex_address, hrp=prefix)


def bech32_address_to_hex_address(address: str):
    """
    Args:
        address: bech32 address string
    """
    prefix = address[0:3]
    return Address.bech32_address_to_address_bytes(address, prefix)


if __name__ == '__main__':
    print(private_key_to_address('bc6c1cfad0ca47375524bb641f7ff6d16b2ffdb140aec190ded46223dcbd99a5', 'lat'))
    # print(hex_address_to_bech32_address('1000000000000000000000000000000000000003', 'atp'))
    hex_address = bech32_address_to_hex_address('atx1ur2hg0u9wt5qenmkcxlp7ysvaw6yupt4xerq62')
    print(f'hex_address = {hex_address}')
    print(hex_address_to_bech32_address(hex_address, 'atp'))

    # print(private_key_to_address('f90fd6808860fe869631d978b0582bb59db6189f7908b578a886d582cb6fccfa', 'atp'))



