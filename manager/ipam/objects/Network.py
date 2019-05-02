import ipaddress
from  manager.ipam.objects.Vlan import Vlan


# These exist in case I have to extend these objects in the future
class Network:

    dhcp_begin = None
    dhcp_end = None

    def __init__(self, network: str, supernet: str, subnets: list, dhcp_enabled: bool, database_conn, **kwargs):
        self.network = network
        self.sql = database_conn
        self.supernet = supernet
        self.subnets = subnets
        if dhcp_enabled:
            self.dhcp_enabled = dhcp_enabled
            self.dhcp_begin = kwargs['dhcp_begin']
            self.dhcp_end = kwargs['dhcp_end']
        else:
            self.dhcp_enabled = False
        if 'vlans' in kwargs.keys():
            self.vlans = kwargs['vlans']

    @staticmethod
    def get(network: str, database_conn):
        returned_network = database_conn.get_network(network)
        if not returned_network:
            return None
        #TODO: sql.get_network is going to merge vlans into this list
        kwargs = {'vlans': returned_network.vlans}
        if returned_network.dhcp_nenabled:
            kwargs['dhcp_end'] = returned_network.dhcp_end
            kwargs['dhcp_begin'] = returned_network.dhcp_begin
            return Network(returned_network.name, returned_network.supernet, returned_network.subnets,
                           returned_network.dhcp_nenabled, **kwargs)
        return Network(returned_network.name, returned_network.dhcp_nenabled, **kwargs)

    def create(self) -> bool:

        if not self.sql.get_network(self.network):
            return self.sql.create_network(self.network)
        return False

    def delete(self) -> bool:
        return self.sql.delete_network(self.network)

    def update(self) -> bool:
        if not self.sql.get_network(self.network):
            return False
        else:
            return self.sql.update_network(self.network)


class IPV6Network(ipaddress.IPv6Network, Network):

    def __init__(self, network: str, supernet: str, subnets: list ,dhcp_enabled: bool, database_conn, **kwargs):
        try:
            super(ipaddress.IPv6Network).__init__(network)
            super(Network).__init__(network, supernet, subnets, dhcp_enabled, database_conn, **kwargs)
        except ipaddress.NetmaskValueError:
            raise ValueError('Netmask incorrect')
        except ValueError:
            raise ValueError('Host bits set')


class IPV4Network(ipaddress.IPv4Network, Network):
    def __init__(self, network: str, supernet: str, subnets: list ,dhcp_enabled: bool, database_conn, **kwargs):
        try:
            super()
        except ipaddress.NetmaskValueError:
            raise ValueError('Netmask incorrect')
        except ValueError:
            raise ValueError('Host bits set')
