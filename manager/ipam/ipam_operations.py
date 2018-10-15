import ipaddress
import objects.IPAddress as IPAddress
import objects.Network as Network
import json
import utils.common
import sql
import utils.types


def create(data):
	data = utils.common.verify_data(data)
	if 'error' in data.keys():
		return json.dumps(error_msg)

	else:
		return json.dumps(error_msg)


@overload
def create_network(networkview: str , network: utils.types.IPV4Network):
	if not sql.get_network(networkview,network.):
		sql.create_network(networkview,network)
		return True
	else:
		return False

@overload
def create_network(networkview: str , network: utils.types.IPV6Network):
	if not sql.get_network(networkview,network.):
		sql.create_network(networkview,network)
		return True
	else:
		return False

def delete_network(networkview, network):
	if sql.get_network(networkview, network):
		sql.delete_network(networkview, network)
		return True
	else:
		return False

def create_v4address(networkview, network, address):
	if sql.get_address(networkview, network, item):
		sql.create_address(networkview, network, item)
		return True
	else:
		return False

def delete_v4address(networkview, network, address)
	if sql.get_address(networkview, network, item):
		sql.create_address(networkview, network, item)
		return True
	else:
		return False

def 

# decorators