import json

def parse_data()

def verify_data(data):
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
	for item in data.keys():
		if type(data[item]) != type(schema[item]):
			return json.dumps({'error':item+' was of incorrect type'})
