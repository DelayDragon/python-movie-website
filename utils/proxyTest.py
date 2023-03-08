import requests

def test_address(address):
    try:
        response = requests.get(address, timeout=5)
        if response.status_code == 200:
            return True
    except requests.exceptions.RequestException:
        pass
    return False

def test_address_pool(address_pool):
    valid_addresses = []
    for address in address_pool:
        if test_address(address):
            valid_addresses.append(address)
    return valid_addresses

