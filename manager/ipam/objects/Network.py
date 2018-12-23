import ipaddress
import manager.sql as sql
from  manager.ipam.objects.Vlan import Vlan
from manager.database.Database import Database

# These exist in case I have to extend these objects in the future
class Network:

    dhcp_begin = None
    dhcp_end = None

    def __init__(self, network: str, dhcp_enabled: bool, **kwargs):
        self.network = network
        if dhcp_enabled:
            self.dhcp_enabled = dhcp_enabled
            self.dhcp_begin = kwargs['dhcp_begin']
            self.dhcp_end = kwargs['dhcp_end']
        else:
            self.dhcp_enabled = False
        if 'vlans' in kwargs.keys():
            self.vlans = kwargs['vlans']

    @staticmethod
    def get(network: str):
        returned_network = sql.get_network(network)
        if not returned_network:
            return None
        #TODO: sql.get_network is going to merge vlans into this list
        kwargs = {'vlans': returned_network.vlans}
        if returned_network.dhcp_nenabled:
            kwargs['dhcp_end'] = returned_network.dhcp_end
            kwargs['dhcp_begin'] = returned_network.dhcp_begin
            return Network(returned_network.name, returned_network.dhcp_nenabled, **kwargs)
        return Network(returned_network.name, returned_network.dhcp_nenabled, **kwargs)

    def create(self) -> bool:
        if not sql.get_network(self.network):
            return sql.create_network(self.network)
        return False

    def delete(self) -> bool:
        return sql.delete_network(self.network)

    def update(self) -> bool:
        if not sql.get_network(self.network):
            return False
        else:
            return sql.update_network(self.network)



class IPV6Network(ipaddress.IPV6Network, Network):

    def __init__(self, network: ipaddress._BaseNetwork, dhcp_enabled: bool, **kwargs):
        try:
            super(ipaddress.IPv6Address).__init__(network)
            super(Network).__init__(network, dhcp_enabled, **kwargs)
        except ipaddress.NetmaskValueError:
            raise ValueError('Netmask incorrect')
        except ValueError:
            raise ValueError('Host bits set')

class IPV4Network(ipaddress.IPV4Network):
    def __init__(self, network: ipaddress._BaseAddress, dhcp_enabled: bool, **kwargs):
        try:
            super().__init__(network)
        except ipaddress.NetmaskValueError:
            raise ValueError('Netmask incorrect')
        except ValueError:
            raise ValueError('Host bits set')
