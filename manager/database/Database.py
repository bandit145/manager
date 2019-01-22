import psycopg2
import logging
from manager.ipam.objects.Vlan import Vlan
from manager.ipam.objects.Network import Network


class Database:

    def __init__(self, host: str, user: str, password: str, dbname: str, port=5432, ssl=True):
        conn_args = {'host':host, 'dbname': dbname, 'user': user, 'password': password,  'port': port}
        if ssl:
            conn_args['sslmode']  = 'require'
        self.connection = psycopg2.connect(**conn_args)
        #do not transact
        self.connection.autocommit = True

    def run_sql_stmt(self, command: str, variables: tuple, ret: bool):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(command, variables)
                if ret:
                    return cursor.fetchall()
                return True
        except psycopg2.Error as error:
            logging.error(error)
            return False

    def create_network(self, network: str, version: int, dhcp_enabled: bool, address_space, dhcp_begin, dhcp_end, view_name: str):
        return self.run_sql_stmt("INSERT into network (view_name, network, version, dhcp_enabled, dhcp_begin, dhcp_end, address_space) VALUES (%s,%s,%s,%s,%s,%s,%s)"
                                 , (view_name, network, version, dhcp_enabled, dhcp_begin, dhcp_end, address_space), False)

    def get_network(self, network: str, view_name: str):
        return self.run_sql_stmt("SELECT view_name, network, version, dhcp_enabled, dhcp_begin, dhcp_end from network  WHERE network=%s AND view_name=%s"
                                 , (network, view_name), True)

    def create_view(self, view_name):
        return self.run_sql_stmt("INSERT into views VALUES (%s)", (view_name,), False)

    def delete_view(self, view_name):
        return self.run_sql_stmt("DELETE FROM views WHERE view_name=%s", (view_name,), False)

    def create_vlan(self, vlan: Vlan, view_name: str):
        return self.run_sql_stmt("INSERT into vlan (name, number, view_name) VALUES (%s,%s,%s)",(vlan.name, vlan.number, view_name), False)

    def get_vlan(self, vlan: Vlan, view_name: str):
        data = self.run_sql_stmt("SELECT name, number from vlan WHERE number=%s AND view_name=%s",(vlan.number, view_name), True)
        if len(data) > 0:
            logging.debug("get_vlan "+str(data))
            return Vlan(name=data[0][0], number=data[0][1])
        return None

    def delete_vlan(self, vlan: Vlan, view_name: str):
        return self.run_sql_stmt("DELETE FROM vlan WHERE number=%s AND view_name=%s", (vlan.number, view_name), False)

    def get_address(self, address: str, view_name: str):
        return self.run_sql_stmt("SELECT address from address WHERE address=%s and view_name=%s",
                          (address, view_name), True)[0][0]

    def get_addresses_in_use(self, network: str, view_name: str):
        return self.run_sql_stmt("""
        SELECT COUNT(*) from address WHERE network_id=(SELECT network_id from network 
        WHERE network=%s and view_name=%s) and view_name=%s and in_use=TRUE """,(network, view_name, view_name),True)[0][0]

    def create_address(self, address: str, version: int, network: Network, in_use: bool,view_name: str):
        return self.run_sql_stmt("""
            INSERT into address (address, version, network_id ,view_name, in_use) VALUES (%s,%s,(SELECT network_id from network WHERE network=%s and view_name=%s),%s,%s) 
        """, (address, version, network.network, view_name, view_name, in_use), False)

    def delete_address(self, address: str, view_name:str ):
        return self.run_sql_stmt("DELETE from address WHERE address=%s and view_name=%s",(address, view_name), False)
