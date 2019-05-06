from manager.ipam.objects.Network import IPV4Network, IPV6Network
from manager.database.Database import Database


def test_ipv4network():
    db = Database('localhost', 'postgres', 'admin', 'manager', 5432, False)
    network = IPV4Network('10.0.0.0/8', None, None, False, db)
    assert(network.create()) == True