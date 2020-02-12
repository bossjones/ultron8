# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrant multi machine configuration

require 'yaml'
config_yml = YAML.load_file(File.open(__dir__ + '/vagrant-config.yml'))

NON_ROOT_USER = 'vagrant'.freeze

stub_name = "ultron8-v"

base_dir = File.dirname(__FILE__)
unless File.exists?("#{base_dir}/vagrant/insecure_ultron8_key")
  system("cd #{base_dir}/vagrant && ssh-keygen -q -t rsa -N '' -f insecure_ultron8_key")
end

# This script to install k8s using kubeadm will get executed after a box is provisioned
$configureBox = <<-SCRIPT
    sudo apt-get update
    sudo apt-get install -y apt-transport-https ca-certificates curl software-properties-common
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
    sudo add-apt-repository "deb [arch=$(dpkg --print-architecture)] https://download.docker.com/linux/$(. /etc/os-release; echo "$ID") $(lsb_release -cs) stable"
    sudo apt-get update
    sudo apt-get install -y docker-ce

    docker info

    # && apt-get install -y docker-ce=$(apt-cache madison docker-ce | grep 17.03 | head -1 | awk '{print $3}')
    # apt-mark hold docker-ce

    # run docker commands as vagrant user (sudo not required)
    sudo usermod -aG docker vagrant

    # install python 3.7
    sudo DEBIAN_FRONTEND=noninteractive add-apt-repository ppa:deadsnakes/ppa
    sudo apt-get update
    sudo apt-get install build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev wget -y
    sudo apt install python3.7 -y

    # install kubeadm
    apt-get install -y apt-transport-https curl
    # apt-mark hold kubelet kubeadm kubectl

    # kubelet requires swap off
    # swapoff -a

    # keep swap off after reboot
    # sudo sed -i '/ swap / s/^\(.*\)$/#\1/g' /etc/fstab

    sudo fallocate -l 2G /swapfile
    sudo dd if=/dev/zero of=/swapfile bs=2048 count=1048576
    sudo chmod 600 /swapfile
    sudo mkswap /swapfile
    sudo swapon /swapfile
    echo "/swapfile swap swap defaults 0 0" | sudo tee -a /etc/fstab
    sudo swapon --show
    sudo free -h

    # ip of this box
    IP_ADDR=`ifconfig enp0s8 | grep Mask | awk '{print $2}'| cut -f2 -d:`
    sudo apt-get -y install python-minimal python-apt
    sudo apt-get install -y \
              bash-completion \
              curl \
              git \
              vim
    sudo DEBIAN_FRONTEND=noninteractive apt-get install -y python-six python-pip

    modprobe ip_vs_wrr
    modprobe ip_vs_rr
    modprobe ip_vs_sh
    modprobe ip_vs
    modprobe nf_conntrack_ipv4
    modprobe bridge
    modprobe br_netfilter

    cat <<EOF >/etc/modules-load.d/k8s_ip_vs.conf
ip_vs_wrr
ip_vs_rr
ip_vs_sh
ip_vs
nf_conntrack_ipv4
EOF

    cat <<EOF >/etc/modules-load.d/k8s_bridge.conf
bridge
EOF

    cat <<EOF >/etc/modules-load.d/k8s_br_netfilter.conf
br_netfilter
EOF
    # NOTE: https://medium.com/@muhammadtriwibowo/set-permanently-ulimit-n-open-files-in-ubuntu-4d61064429a
    # TODO: Put into playbook
    echo "65535" | sudo tee /proc/sys/fs/file-max
    echo "session required pam_limits.so" | sudo tee -a /etc/pam.d/common-session

    sudo sysctl -w vm.min_free_kbytes=1024000
    sudo sync; sudo sysctl -w vm.drop_caches=3; sudo sync
    sudo mkdir -p ~vagrant/dev
    sudo -i -u vagrant git clone https://github.com/viasite-ansible/ansible-role-zsh ~vagrant/dev/ansible-role-zsh
    sudo chown vagrant:vagrant -Rv ~vagrant
    sudo apt-get install software-properties-common -y
    sudo apt-add-repository ppa:ansible/ansible -y
    sudo apt-get update
    sudo apt-get install ansible -y
    sudo mkdir -p /etc/ansible/roles
    sudo chown vagrant:vagrant -Rv /etc/ansible/roles

    sudo -i -u vagrant git clone https://github.com/samoshkin/tmux-config.git ~vagrant/dev/tmux-config
    echo "------------------Finished------------------"
    echo "Now run ansible-galaxy"
    echo 'vagrant:vagrant' | chpasswd
SCRIPT

Vagrant.configure(2) do |config|
  # set auto update to false if you do NOT want to check the correct additions version when booting this machine
  # config.vbguest.auto_update = true

  config.vm.synced_folder ".", "/srv/vagrant_repos/ultron8", disabled: false

  config_yml[:vms].each do |name, settings|
    # use the config key as the vm identifier
    config.vm.define name.to_s, autostart: true, primary: true do |vm_config|
      config.ssh.insert_key = false
      vm_config.vm.usable_port_range = (2200..2250)

      # This will be applied to all vms

      # set auto_update to false, if you do NOT want to check the correct
      # additions version when booting this machine
      vm_config.vbguest.auto_update = true

      vm_config.vm.box = settings[:box]
      vm_config.disksize.size = '15GB'


      vm_config.vm.network 'private_network', ip: settings[:eth1]

      # DISABLED:: # # INFO: Docker ports
      # DISABLED:: # config.vm.network "forwarded_port", guest: 2375, host: settings[:dockerport1]
      # DISABLED:: # config.vm.network "forwarded_port", guest: 2376, host: settings[:dockerport2]

      vm_config.vm.hostname = "#{settings[:hostname]}.#{stub_name}"

      config.vm.provider 'virtualbox' do |v|
        # make sure that the name makes sense when seen in the vbox GUI
        v.name = "#{settings[:hostname]}.#{stub_name}"

        v.gui = false
        v.customize ['modifyvm', :id, '--groups', '/Ultron Development']
        v.customize ['modifyvm', :id, '--memory', settings[:mem]]
        v.customize ['modifyvm', :id, '--cpus', settings[:cpu]]
      end

      hostname_with_hyenalab_tld = "#{settings[:hostname]}.bosslab.com"

      aliases = [hostname_with_hyenalab_tld, settings[:hostname], "#{settings[:hostname]}.#{stub_name}"]

      if Vagrant.has_plugin?('vagrant-hostsupdater')
        puts 'IM HERE BABY'
        config.hostsupdater.aliases = aliases
        vm_config.hostsupdater.aliases = aliases
      elsif Vagrant.has_plugin?('vagrant-hostmanager')
        puts 'IM HERE HONEY'
        vm_config.hostmanager.enabled = true
        vm_config.hostmanager.manage_host = true
        vm_config.hostmanager.manage_guests = true
        vm_config.hostmanager.ignore_private_ip = false
        vm_config.hostmanager.include_offline = true
        vm_config.hostmanager.aliases = aliases
      end

      if "#{settings[:hostname]}.#{stub_name}" == "master.#{stub_name}"
         # pre-configure our playground trond
         vm_config.vm.provision :shell, inline: "install -d -m 2750 -o vagrant -g vagrant /var/lib/ultron8"
         vm_config.vm.provision :shell, inline: "install -d -m 2750 -o vagrant -g vagrant /var/log/ultron8"
         vm_config.vm.provision :shell, privileged: false, inline: "install -m 600 /srv/vagrant_repos/ultron8/vagrant/insecure_ultron8_key /home/vagrant/.ssh/id_rsa"
         vm_config.vm.provision :shell, inline: "install -m 644 /srv/vagrant_repos/ultron8/vagrant/hosts /etc/hosts"

         # Fire up the requisite ssh-agent and load our private key.
         vm_config.vm.provision :shell, privileged: false, inline: "ssh-agent > /var/lib/ultron8/ssh-agent.sh"
         vm_config.vm.provision :shell, privileged: false, inline: ". /var/lib/ultron8/ssh-agent.sh && ssh-add /home/vagrant/.ssh/id_rsa"
      end

      vm_config.vm.provision 'shell', inline: $configureBox

      vm_config.vm.provision :shell, privileged: false, inline: "cat /srv/vagrant_repos/ultron8/vagrant/insecure_ultron8_key.pub >> /home/vagrant/.ssh/authorized_keys"
      vm_config.vm.provision :shell, inline: "install -m 644 /srv/vagrant_repos/ultron8/vagrant/hosts /etc/hosts"
      vm_config.vm.provision :shell, inline: "install -m 755 /srv/vagrant_repos/ultron8/vagrant/sync_code.sh /usr/local/bin/sync_ultron8.sh"
      vm_config.vm.provision :shell, inline: "install -m 755 /srv/vagrant_repos/ultron8/vagrant/sync_code.sh /usr/local/bin/sync_code.sh"
      vm_config.vm.provision :shell, inline: "cd && rsync -r --exclude .vagrant --exclude .git /srv/vagrant_repos/ultron8/ ~/ultron8/ && cd ~/ultron8 && ls -lta"
    end
  end
end
