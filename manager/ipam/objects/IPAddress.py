import ipaddress

class V4(ipaddress.IPV4Address):

	def __init__(self, address):
		try:
			super().__init__(address)
		except ipaddress.AddressValueError:
			raise ValueError('incorrect value for ipv6 address')
		self.address = address

class V6(ipaddress.IPV6Address):

	def __init__(self, address):
		try:
			super().__init__(address)
		except ipaddress.AddressValueError:
			raise ValueError('incorrect value for ipv6 address')
		self.address = address
