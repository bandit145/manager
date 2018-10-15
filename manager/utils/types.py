from typing import NewType
import manager.ipam.objects.IPAddress as IPAddress
import manager.ipam.objects.Network as Network

IPV4Address = NewType('IPV4Address',IPAddress.V4)
IPV6Address = NewType('IPV6Address',IPV6Address.V6)
IPV6Network = NewType('IPV6Network',Network.V6)
IPV4Network = NewType('IPV4Network',Network.V4)