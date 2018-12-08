import ipaddress
import manager.objects.IPAddress as IPAddress
import manager.objects.Network as Network
import json
import manager.utils.common
import manager.objects.sql as sql


def create_network(networkview: str, network: dict) -> bool:
    if not sql.get_network(networkview, network):
        sql.create_network(networkview, network)
        return True
    return False


def network_exist(networkview: str, network: dict) -> bool:
    if not sql.get_network(networkview, network):
        return False
    return False


def update_network(networkview: str, network: dict) -> bool:
    existing_network = sql.get_network(networkview, network):
    if existing_network:
        if network != existing_network:
            sql.update_network(networkview, network)
            return True
        return False

def delete_network(networkview: str, network: dict) -> bool:
    if sql.get_network(networkview, network):
        sql.delete_network(networkview, network)
        return True
    return False

def get_network(networkview: str, network: ipaddress._BaseNetwork) -> ipaddress._BaseNetwork:
    return sql.get_network(networkview, network)

def create_address(networkview: str, address)