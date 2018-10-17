import ipaddress
import manager.objects.IPAddress as IPAddress
import manager.objects.Network as Network
import json
import manager.utils.common
import manager.objects.sql as sql



def create(data):
	data = utils.common.verify_data(data)
	if 'error' in data.keys():
		return json.dumps(error_msg)
	for item in data:
		if data


def create_network(networkview: -> str, network: -> ipaddress._BaseNetwork) -> bool
	if not sql.get_network(networkview, network):
		sql.create_network(networkview, network)
		return True
	return False

def network_exist(networkview: -> str, network: -> ipaddress._BaseNetwork) - > bool
	if not sql.get_network(networkview, network):
		return False
	return False

def update_network(networkview: -> str, network: -> ipaddress._BaseNetwork): -> bool
	return sql.update_network(networkview, network)

def delete_network(networkview: -> str, network: -> ipaddress._BaseNetwork): -> bool
	if sql.get_network(networkview, network):
		sql.delete_network(networkview, network)
		return True
	return False

# decorators