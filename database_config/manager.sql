CREATE DATABASE manager;
USE manager;

CREATE TABLE network (
  network_id SERIAL PRIMARY KEY,
	network cidr NOT NULL,
	version  smallint NOT NULL,
	dhcp_enabled boolean NOT NULL,
	dhcp_begin ident NOT NULL,
	dhcp_end ident NOT NULL,
);

CREATE TABLE vlan (
  vlan_id SERIAL PRIMARY KEY,
  vlan_number bigint NOT NULL,
  name varchar(50) NOT NULL,
  network_id int REFERENCES  network(network_id)

);

CREATE TABLE vlan_network (
  vlan_id int REFERENCES vlan(vlan_id) ON UPDATE CASCADE ON DELETE CASCADE,
  network_id int REFERENCES network(network_id) ON UPDATE CASCADE ON DELETE CASCADE

);

CREATE TABLE address (
	address ident NOT NULL,
	version smallint NOT NULL,
	network cidr NOT NULL,
	view varchar(50) NOT NULL,
	CONSTRAINT fk_network_view
		FOREIGN KEY (view) REFERENCES networkview(name)
		ON DELETE CASCADE,
	CONSTRAINT fk_network
		FOREIGN KEY (network) REFERENCES network(network)
		ON DELETE CASCADE,
	CONSTRAINT address_unique UNIQUE (network,address)
);