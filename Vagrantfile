# -*- mode: ruby -*-
# vi: set ft=ruby :

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure("2") do |config|

     config.vm.define "server1" do |client|
        client.vm.provider "virtualbox" do |vm|
            vm.memory = 1024
            vm.cpus = 1
        end
        client.vm.box = "centos/7"
        client.vm.network "private_network", ip: "192.168.50.2"
        config.vm.provision "shell", inline: "yum -y install epel-release && yum -y  install https://download.postgresql.org/pub/repos/yum/11/redhat/rhel-7-x86_64/pgdg-centos11-11-2.noarch.rpm"
        config.vm.provision "shell", inline: "yum -y install postgresql11-server"
        config.vm.provision "shell", inline: "/usr/pgsql-11/bin/postgresql-11-setup initdb"
        config.vm.provision "shell", inline: "echo \"listen_addresses = '*'\" >> /var/lib/pgsql/11/data/postgresql.conf"
        config.vm.provision "shell", inline: "service postgresql-11 start"
     end
end
