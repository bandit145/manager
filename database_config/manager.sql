CREATE DATABASE ipam;
USE ipam;

# create network-views

CREATE TABLE networkview (
	name varchar(50) NOT NULL,
	PRIMARY KEY(name)
);

CREATE TABLE network (
	network varchar(41) NOT NULL,
	version  smallint NOT NULL,
	view varchar(50) NOT NULL, 
	dhcpbegin varchar(41),
	dhcpend varchar(41),
	CONSTRAINT fk_network_view
		FOREIGN KEY (view) REFERENCES networkview(name)
		ON DELETE CASCADE,
	CONSTRAINT network_unique UNIQUE (network, view)
);

CREATE TABLE address (
	address varchar(39) NOT NULL,
	version smallint NOT NULL,
	network varchar(41) NOT NULL,
	view varchar(50) NOT NULL,
	CONSTRAINT fk_network_view
		FOREIGN KEY (view) REFERENCES networkview(name)
		ON DELETE CASCADE,
	CONSTRAINT fk_network
		FOREIGN KEY (network) REFERENCES network(network)
		ON DELETE CASCADE,
	CONSTRAINT address_unique UNIQUE (network,view,address)
);