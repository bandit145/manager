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

    def run_sql_stmt(self, commAND: str, variables: tuple, ret: bool):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(commAND, variables)
                if ret:
                    return cursor.fetchall()
                return True
        except psycopg2.Error as error:
            logging.error(error)
            return False

    def create_network(self, network: str, supernet: str, version: int, dhcp_enabled: bool, address_space, dhcp_begin, dhcp_end, view_name: str):
        if supernet:
            response = self.run_sql_stmt("INSERT INTO network (view_name, network, version, supernet, dhcp_enabled, dhcp_begin, dhcp_end, address_space) VALUES (%s,%s,%s,(SELECT network_id FROM network WHERE network=%s AND view_name=%s),%s,%s,%s,%s)"
                                 , (view_name, network, version, supernet, view_name, dhcp_enabled, dhcp_begin, dhcp_end, address_space), False)
        else:
            response = self.run_sql_stmt("INSERT INTO network (view_name, network, version, supernet, dhcp_enabled, dhcp_begin, dhcp_end, address_space) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
                                 , (view_name, network, version, supernet, dhcp_enabled, dhcp_begin, dhcp_end, address_space), False)
        return response

    def add_avail_pool_member(self, network: str, availability_pool: str, view_name: str):
        return self.run_sql_stmt("""INSERT into availability_pools_networks (avail_id, network_id) 
                VALUES ((SELECT avail_id FROM availability_pool WHERE name=%s AND view_name=%s), 
                    (SELECT network_id FROM network WHERE network=%s AND view_name=%s))""", (availability_pool, view_name, network, view_name) ,False)

    def delete_avail_pool_member(self, network:str, availability_pool: str, view_name: str):
        return self.run_sql_stmt("""DELETE FROM availability_pools_networks 
            WHERE network_id=(SELECT network_id FROM network WHERE network=%s AND view_name=%s) 
            AND avail_id=((SELECT avail_id FROM availability_pool WHERE name=%s AND view_name=%s))""", (network, view_name, availability_pool, view_name), False)

    def delete_network(self, network: str, view_name: str):
        return self.run_sql_stmt("DELETE FROM network WHERE network=%s AND view_name=%s", (network, view_name), False)

    def get_network(self, network: str, view_name: str):
        return self.run_sql_stmt("SELECT view_name, network, version, dhcp_enabled, dhcp_begin, dhcp_end FROM network  WHERE network=%s AND view_name=%s"
                                 , (network, view_name), True)

    def create_view(self, view_name):
        return self.run_sql_stmt("INSERT into views VALUES (%s)", (view_name,), False)

    def delete_view(self, view_name):
        return self.run_sql_stmt("DELETE FROM views WHERE view_name=%s", (view_name,), False)

    def create_vlan(self, vlan: Vlan, view_name: str):
        return self.run_sql_stmt("INSERT into vlan (name, number, view_name) VALUES (%s,%s,%s)",(vlan.name, vlan.number, view_name), False)

    def get_vlan(self, vlan: Vlan, view_name: str):
        data = self.run_sql_stmt("SELECT name, number FROM vlan WHERE number=%s AND view_name=%s",(vlan.number, view_name), True)
        if len(data) > 0:
            logging.debug("get_vlan "+str(data))
            return Vlan(name=data[0][0], number=data[0][1])
        return None

    def delete_vlan(self, vlan: Vlan, view_name: str):
        return self.run_sql_stmt("DELETE FROM vlan WHERE number=%s AND view_name=%s", (vlan.number, view_name), False)

    def get_address(self, address: str, view_name: str):
        return self.run_sql_stmt("SELECT address FROM address WHERE address=%s AND view_name=%s",
                          (address, view_name), True)[0][0]

    def get_addresses_in_use(self, network: str, view_name: str):
        return self.run_sql_stmt("""
        SELECT COUNT(*) FROM address WHERE network_id=(SELECT network_id FROM network 
        WHERE network=%s AND view_name=%s) AND view_name=%s""",(network, view_name, view_name),True)[0][0]

    def get_networks_FROM_avail_pool(self, availability_pool: str, view_name: str):
        return self.run_sql_stmt("SELECT avail_id FROM availability_pool WHERE name=%s AND view_name=%s")

    def create_address(self, address: str, version: int, network: Network, view_name: str):
        return self.run_sql_stmt("INSERT into address (address, version, network_id ,view_name) VALUES (%s,%s,(SELECT network_id FROM network WHERE network=%s AND view_name=%s),%s)"
             , (address, version, network.network, view_name, view_name), False)

    def delete_address(self, address: str, view_name:str ):
        return self.run_sql_stmt("DELETE FROM address WHERE address=%s AND view_name=%s", (address, view_name), False)

    def create_avail_pool(self, name: str, view_name: str):
        return self.run_sql_stmt("INSERT into availability_pool (name, view_name) VALUES (%s, %s)", (name, view_name), False)

    def get_avail_pool(self, name: str, view_name: str):
        return self.run_sql_stmt("SELECT name FROM availability_pool WHERE name=%s AND view_name=%s", (name, view_name), True)

    def delete_avail_pool(self, name: str, view_name: str):
        return self.run_sql_stmt("DELETE FROM availability_pool WHERE name=%s AND view_name=%s", (name, view_name), False)
