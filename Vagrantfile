# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  # All Vagrant configuration is done here. The most common configuration
  # options are documented and commented below. For a complete reference,
  # please see the online documentation at vagrantup.com.

  config.vm.box = "ubuntu/trusty64"
  # Every Vagrant virtual environment requires a box to build off of.
  config.vm.provider "virtualbox" do |vb|
    # required for lxml compile
    vb.memory = 2048
  end
  config.vm.provider "libvirt" do |vb, override_libvirt|
    override_libvirt.vm.box = "naelyn/ubuntu-trusty64-libvirt"
    # required for lxml compile
    vb.memory = 2048
  end
  config.vm.provider "docker" do |vb, override_docker|
    vb.image = "library/ubuntu:latest"
    # required for lxml compile
    vb.memory = 2048
  end

  config.vm.define "machine"
  config.vm.provision "ansible_local" do |ansible|
    ansible.extra_vars = {
      project_path: "/vagrant",
      vagrant: 1
    }
    ansible.version = "latest"
    ansible.playbook = "ansible/playbook.yml"
    ansible.groups = { "irp2" => ["machine"] }
  end
  # Disable automatic box update checking. If you disable this, then
  # boxes will only be checked for updates when the user runs
  # `vagrant box outdated`. This is not recommended.
  # config.vm.box_check_update = false

  # Create a forwarded port mapping which allows access to a specific port
  # within the machine from a port on the host machine. In the example below,
  # accessing "localhost:8080" will access port 80 on the guest machine.
  config.vm.network "forwarded_port", guest: 5000, host: 5000
  config.vm.network "forwarded_port", guest: 80, host: 8080
  config.vm.network "forwarded_port", guest: 8983, host: 8983

  # Create a private network, which allows host-only access to the machine
  # using a specific IP.
  # config.vm.network "private_network", ip: "192.168.33.10"

  # Create a public network, which generally matched to bridged network.
  # Bridged networks make the machine appear as another physical device on
  # your network.
  # config.vm.network "public_network"

  # If true, then any SSH connections made will enable agent forwarding.
  # Default value: false
  config.ssh.forward_agent = true

  # Share an additional folder to the guest VM. The first argument is
  # the path on the host to the actual folder. The second argument is
  # the path on the guest to mount the folder. And the optional third
  # argument is a set of non-required options.
  # config.vm.synced_folder "../data", "/vagrant_data"

end
