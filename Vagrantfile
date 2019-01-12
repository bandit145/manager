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
        config.vm.provision "ansible_local" do |ansible|
            ansible.limit = "all,localhost"
            ansible.become = true
            ansible.playbook = "postgres.yml"
        end
     end
end
