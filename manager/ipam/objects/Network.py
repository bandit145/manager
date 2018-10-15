import ipaddress

# These exist in case I have to extend these objects in the future

class V6(ipaddress.IPV6Network):

	def __init__(self, network):
		try:
			super().__init__(network)
		except ipaddress.NetmaskValueError:
			raise ValueError('Netmask incorrect')
		except ValueError:
			raise ValueError('Host bits set')

class V4(ipaddress.IPV4Network):
	def __init__(self, network):
		try:
			super().__init__(network)
		except ipaddress.NetmaskValueError:
			raise ValueError('Netmask incorrect')
		except ValueError:
			raise ValueError('Host bits set')