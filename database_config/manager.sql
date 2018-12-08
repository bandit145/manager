CREATE DATABASE ipam;
USE ipam;

CREATE TABLE network (
	network varchar(41) NOT NULL,
	version  smallint NOT NULL,
	dhcp_enabled boolean NOT NULL,
	dhcp_begin varchar(41),
	dhcp_end varchar(41),
	CONSTRAINT network_unique UNIQUE (network)
);

CREATE TABLE vlan (
  number bigint NOT NULL,
  name varchar(50) NOT NULL,
  network varchar(41) NOT NULL,
  CONSTRAINT number_unique UNIQUE (number),
  CONSTRAINT fk_network
    FOREIGN KEY (network) REFERENCES network (network)

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
	CONSTRAINT address_unique UNIQUE (network,address)
);