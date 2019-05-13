CREATE DATABASE manager;
\connect manager;

CREATE TABLE views (
  	view_name text PRIMARY KEY
);

CREATE TABLE availability_pool (
	avail_id serial PRIMARY KEY,
	name text,
	view_name text REFERENCES views(view_name) ON DELETE CASCADE,
	UNIQUE (name, view_name)
);

CREATE TABLE network (
  	network_id serial PRIMARY KEY,
  	view_name text REFERENCES views(view_name) ON DELETE CASCADE,
	network cidr NOT NULL,
	version  smallint NOT NULL CHECK (version = 4 OR version = 6),
	address_space int NOT NULL,
	supernet int REFERENCES network(network_id) ON DELETE CASCADE,
	dhcp_enabled boolean NOT NULL,
	dhcp_begin inet,
	dhcp_end inet,
	UNIQUE (network, view_name)
);

CREATE TABLE availability_pools_networks (
	avail_id serial REFERENCES availability_pool(avail_id) on DELETE CASCADE,
	network_id int REFERENCES network(network_id) ON DELETE CASCADE
);

CREATE TABLE vlan (
	vlan_id serial PRIMARY KEY,
 	number bigint NOT NULL,
  	name text NOT NULL,
  	view_name text REFERENCES views(view_name) ON DELETE CASCADE,
  	network_id int REFERENCES  network(network_id)
);

CREATE TABLE vlan_network (
  	vlan_id int REFERENCES vlan(vlan_id) ON DELETE CASCADE,
  	network_id int REFERENCES network(network_id) ON DELETE CASCADE
);

CREATE TABLE address (
  	address_id serial PRIMARY KEY,
	address inet NOT NULL,
	version smallint NOT NULL CHECK (version = 4 OR version = 6),
	network_id int NOT NULL REFERENCES network(network_id) ON DELETE  CASCADE ,
	view_name text REFERENCES views(view_name) ON DELETE CASCADE,
	UNIQUE (address, view_name)
);