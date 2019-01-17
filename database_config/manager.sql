CREATE DATABASE manager;
\connect manager;

CREATE TABLE views (
  view_name varchar PRIMARY KEY
);


CREATE TABLE network (
  network_id SERIAL PRIMARY KEY,
  view_name varchar references views(view_name) ON DELETE CASCADE,
	network cidr NOT NULL,
	version  smallint NOT NULL CHECK (version = 4 OR version = 6),
	address_space int NOT NULL,
	subnets varchar[],
	supernet serial,
	dhcp_enabled boolean NOT NULL,
	dhcp_begin inet,
	dhcp_end inet,
	UNIQUE (network, view_name)
);

CREATE TABLE vlan (
  vlan_id SERIAL PRIMARY KEY,
  vlan_number bigint NOT NULL,
  name varchar(50) NOT NULL,
  view_name varchar references views(view_name) on DELETE CASCADE,
  network_id int REFERENCES  network(network_id)
);

CREATE TABLE vlan_network (
  vlan_id int REFERENCES vlan(vlan_id) ON UPDATE CASCADE ON DELETE CASCADE,
  network_id int REFERENCES network(network_id) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE address (
  address_id SERIAL PRIMARY KEY,
	address inet NOT NULL,
	version smallint NOT NULL CHECK (version = 4 OR version = 6),
	network_id serial NOT NULL references network(network_id),
	view_name varchar references views(view_name) on DELETE CASCADE,
	UNIQUE (address, view_name)
);