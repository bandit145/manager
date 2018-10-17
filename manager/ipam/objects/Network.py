import ipaddress
import manager.sql as sql
from manager.database.Database import Database

# These exist in case I have to extend these objects in the future

class IPV6Network(ipaddress.IPV6Network):

	def __init__(self, network):
		try:
			super().__init__(network)
		except ipaddress.NetmaskValueError:
			raise ValueError('Netmask incorrect')
		except ValueError:
			raise ValueError('Host bits set')


class IPV4Network(ipaddress.IPV4Network):
	def __init__(self, network):
		try:
			super().__init__(network)
		except ipaddress.NetmaskValueError:
			raise ValueError('Netmask incorrect')
		except ValueError:
			raise ValueError('Host bits set')