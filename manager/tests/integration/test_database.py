import pytest
import logging
import unittest.mock as mock
from manager.database.Database import Database

def test_create_view():
    db = Database('localhost', 'postgres', 'admin', 'manager', 5432, False)
    assert(db.create_view('test_view')) == True
    assert(db.create_view('test_view_two')) == True

#  network: str, version: int, dhcp_enabled: bool, dhcp_begin: str, dhcp_end: str, view_name: str
def test_network_sql():
    db = Database('localhost', 'postgres', 'admin', 'manager', 5432, False)
    assert(db.create_network('192.168.1.0/24', 4, False, 254, None, None, 'test_view')) == True
    #try and create duplicate network
    assert (db.create_network('192.168.1.0/24', 4, False, 254, None, None, 'wat')) == False
    assert(db.get_network('192.168.1.0/24', 'test_view'))[0] == ('test_view', '192.168.1.0/24', 4, False, None, None)

def test_addresses():
    db = Database('localhost', 'postgres', 'admin', 'manager', 5432, False)
    network = mock.Mock()
    network.network = '192.168.1.0/24'
    assert(db.create_address('192.168.1.2', 4, network, 'test_view')) == True
    assert(db.get_address('192.168.1.2', 'test_view'))[0] == ('192.168.1.2',)

def test_destroy_view():
     db = Database('localhost', 'postgres', 'admin', 'manager', 5432, False)
     assert(db.delete_view('test_view')) == True
     assert (db.delete_view('test_view_two')) == True
     assert (len(db.get_network('192.168.1.0/24', 'test_view'))) == 0

