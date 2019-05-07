CREATE DATABASE manager;
\connect manager;

CREATE EXTENSION ltree;

CREATE TABLE views (
  	view_name text PRIMARY KEY
);

CREATE TABLE availability_pool (
	avail_id SERIAL PRIMARY KEY,
	name text,
	view_name text references views(view_name) on DELETE CASCADE,
	UNIQUE (name, view_name)
);

CREATE TABLE network (
  	network_id SERIAL PRIMARY KEY,
  	view_name text references views(view_name) ON DELETE CASCADE,
	network cidr NOT NULL,
	version  smallint NOT NULL CHECK (version = 4 OR version = 6),
	address_space int NOT NULL,
	supernet int references network(network_id) ON DELETE CASCADE,
	dhcp_enabled boolean NOT NULL,
	dhcp_begin inet,
	dhcp_end inet,
	UNIQUE (network, view_name)
);

CREATE TABLE availability_pools_networks (
	avail_id SERIAL REFERENCES availability_pool(avail_id) on DELETE CASCADE,
	network_id int REFERENCES network(network_id) ON DELETE CASCADE
);

CREATE TABLE vlan (
	vlan_id SERIAL PRIMARY KEY,
 	number bigint NOT NULL,
  	name text NOT NULL,
  	view_name text references views(view_name) on DELETE CASCADE,
  	network_id int REFERENCES  network(network_id)
);

CREATE TABLE vlan_network (
  	vlan_id int REFERENCES vlan(vlan_id) ON DELETE CASCADE,
  	network_id int REFERENCES network(network_id) ON DELETE CASCADE
);

CREATE TABLE address (
  	address_id SERIAL PRIMARY KEY,
	address inet NOT NULL,
	version smallint NOT NULL CHECK (version = 4 OR version = 6),
	network_id int NOT NULL references network(network_id) on DELETE  CASCADE ,
	view_name text references views(view_name) on DELETE CASCADE,
	UNIQUE (address, view_name)
);