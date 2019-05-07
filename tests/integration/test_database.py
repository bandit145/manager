import pytest
import unittest.mock as mock
from manager.ipam.objects.Vlan import Vlan
from manager.database.Database import Database

def test_create_view():
    db = Database('localhost', 'postgres', 'admin', 'manager', 5432, False)
    assert(db.create_view('test_view')) == True
    assert(db.create_view('test_view_two')) == True

#  network: str, version: int, dhcp_enabled: bool, dhcp_begin: str, dhcp_end: str, view_name: str
def test_network_sql():
    db = Database('localhost', 'postgres', 'admin', 'manager', 5432, False)
    # create network tree
    assert (db.create_network('10.0.0.0/8', None, 4, False, 16777216, None, None, 'test_view'))
    assert (db.create_network('10.4.0.0/16', '10.0.0.0/8', 4, False, 65536, None, None, 'test_view'))
    assert (db.create_network('10.5.0.0/16', '10.0.0.0/8', 4, False, 65536, None, None, 'test_view'))
    assert (db.create_network('10.5.1.0/24', '10.5.0.0/16' ,4, False, 254, None, None, 'test_view'))
    assert (db.create_network('10.4.1.0/24', '10.4.0.0/16' ,4, False, 254, None, None, 'test_view'))
    assert (db.create_network('10.4.2.0/24', '10.4.0.0/16' ,4, False, 254, None, None, 'test_view'))
    assert (db.get_network('10.4.1.0/24', 'test_view'))[0] == ('test_view', '10.4.1.0/24', 4, False, None, None)
    # delete
    assert (db.delete_network('10.4.1.0/24', 'test_view'))
    assert (db.get_network('10.4.1.0/24', 'test_view')) == []
    # delete and verify record below is gone
    assert (db.delete_network('10.5.0.0/16', 'test_view'))
    assert (db.get_network('10.5.1.0/24', 'test_view')) == []

def test_addresses():
    db = Database('localhost', 'postgres', 'admin', 'manager', 5432, False)
    network = mock.Mock()
    network.network = '10.4.2.0/24'
    assert (db.create_address('10.4.2.2', 4, network, 'test_view'))
    # create disabled address to verify that this only returns one
    assert (db.create_address('10.4.2.3', 4, network, 'test_view'))
    assert (db.get_address('10.4.2.2', 'test_view')) == '10.4.2.2'

def test_get_address_in_use():
    db = Database('localhost', 'postgres', 'admin', 'manager', 5432, False)
    assert(db.get_addresses_in_use('10.4.2.0/24', 'test_view')) == 2

def test_avail_pool():
    db = Database('localhost', 'postgres', 'admin', 'manager', 5432, False)
    assert (db.create_avail_pool('NY-DC', 'test_view'))
    assert (db.get_avail_pool('NY-DC', 'test_view'))[0] == ('NY-DC',)
    assert (db.delete_avail_pool('NY-DC', 'test_view'))
    assert (db.create_avail_pool('NY-DC', 'test_view'))
    assert (db.add_avail_pool_member('10.5.0.0/16', 'NY-DC', 'test_view'))
    assert (db.delete_avail_pool_member('10.5.0.0/16', 'NY-DC', 'test_view'))

def test_vlan():
    db = Database('localhost', 'postgres', 'admin', 'manager', 5432, False)
    vlan = Vlan('servers', 60)
    assert(db.create_vlan(vlan, 'test_view')) == True
    assert(db.get_vlan(vlan, 'test_view')) == vlan
    assert(db.delete_vlan(vlan, 'test_view')) == True
    assert(db.get_vlan(vlan, 'test_view')) is None

def test_destroy_view():
     db = Database('localhost', 'postgres', 'admin', 'manager', 5432, False)
     assert(db.delete_view('test_view')) == True
     assert (db.delete_view('test_view_two')) == True
     assert (db.get_network('10.0.0.0/8', 'test_view')) ==[]
