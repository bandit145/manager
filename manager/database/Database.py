import psycopg2
import ipaddress
from manager.ipam.objects.Vlan import Vlan


class Database:

    def __init__(self, host: str, user: str, password: str, dbname: str, port=5432, ssl=True):
        conn_args = {'host':host, 'dbname': dbname, 'user': user, 'password': password,  'port': port}
        if ssl:
            conn_args['sslmode']  = 'require'
        self.connection = psycopg2.connect(**conn_args)

    def run_sql_stmt(self, command: str, variables: tuple, ret: bool):
        try:
            cursor = self.connection.cursor()
            cursor.execute(command, variables)
            if ret:
                return cursor.fetchall()
            cursor.close()
            return True
        except Exception as error:
            print(error)
            return False

    def create_network(self, network: str, version: int, dhcp_enabled: bool, dhcp_begin: str, dhcp_end: str, view_name: str):
        return self.run_sql_stmt("INSERT into network  VALUES ('%s','%s','%s','%s','%s','%s')", (view_name, network, version, dhcp_enabled, dhcp_begin, dhcp_end))

    def get_network(self, network: str, view_name: str):
        return self.run_sql_stmt("SELECT * from network WHERE network=%s AND view_name=%s", (network, view_name))

    def create_view(self, view_name):
        return self.run_sql_stmt("INSERT into views VALUES ('%s')", (view_name))

    def delete_view(self, view_name):
        return self.run_sql_stmt("DELETE FROM views WHERE view_name=%s", (view_name))

    def create_vlan(self, vlan: Vlan, view_name: str):
        return self.run_sql_stmt("INSERT into vlan VALUES ('%s','%s')",(vlan.name, vlan.number, view_name))

    def get_vlan(self, vlan: Vlan, view_name: str):
        data = self.run_sql_stmt("SELECT * from vlan WHERE vlan_number=%s AND view_name=%s",(vlan.number, view_name))
        return Vlan(name=data[0], number=data[1])

    def delete_vlan(self, vlan: Vlan, view_name: str):
        return self.run_sql_stmt("DELETE FROM vlan WHERE vlan_number=%s AND view_name=%s", (vlan.number, view_name))
