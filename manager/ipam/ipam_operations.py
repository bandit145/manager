import ipaddress

def verify_ipam_data(data):
	''' ipam Datastructure
	network:
	{
		"type":"network",
		"view":"networkview",
		"network":"network/cidr"
	}
	ipaddress:
	{
		"type":"address",
		"view":"networkview"
		"network":"network/cidr",
		"address":"192.168.50.2"
	}

	'''

def create(data):
