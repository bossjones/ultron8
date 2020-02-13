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
    sudo apt-get install -y apt-transport-https curl unzip wget
    sudo fallocate -l 4G /swapfile
    sudo dd if=/dev/zero of=/swapfile bs=2048 count=1048576
    sudo chmod 600 /swapfile
    sudo mkswap /swapfile
    sudo swapon /swapfile
    echo "/swapfile swap swap defaults 0 0" | sudo tee -a /etc/fstab
    sudo swapon --show
    sudo free -h


    DEBIAN_FRONTEND=noninteractive apt-get upgrade -yqq \
    && apt-get install -y --no-install-recommends \
        openssh-client \
        procps && \
        apt-get update && apt-get install -y --no-install-recommends \
        autoconf \
        automake \
        bzip2 \
        file \
        g++ \
        gcc \
        imagemagick \
        libbz2-dev \
        libc6-dev \
        libcurl4-openssl-dev \
        libdb-dev \
        libevent-dev \
        libffi-dev \
        libgeoip-dev \
        libglib2.0-dev \
        libjpeg-dev \
        libkrb5-dev \
        liblzma-dev \
        libmagickcore-dev \
        libmagickwand-dev \
        libmysqlclient-dev \
        libncurses-dev \
        libpng-dev \
        libpq-dev \
        libreadline-dev \
        libsqlite3-dev \
        libtool \
        libwebp-dev \
        libxml2-dev \
        libxslt-dev \
        libyaml-dev \
        make \
        patch \
        xz-utils \
        zlib1g-dev \
        bash

    sudo apt-get update && \
    sudo apt-get install -y \
      build-essential \
      cmake \
      tmux \
      zsh \
      clang \
      manpages-dev

    echo "===> gcc for cgo..." && \
    sudo apt-get update && \
    sudo apt-get install -y \
      g++ \
      gcc \
      libc6-dev \
      make \
      pkg-config \
      ninja-build

    sudo apt-get install -y xclip ca-certificates curl software-properties-common zsh
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
    sudo add-apt-repository "deb [arch=$(dpkg --print-architecture)] https://download.docker.com/linux/$(. /etc/os-release; echo "$ID") $(lsb_release -cs) stable"
    sudo apt-get update
    sudo apt-get install -y docker-ce

    docker info

    # run docker commands as vagrant user (sudo not required)
    sudo usermod -aG docker vagrant

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
    echo "skip_global_compinit=1" | sudo tee -a /etc/zsh/zshenv

    sudo sysctl -w vm.min_free_kbytes=1024000
    sudo sync; sudo sysctl -w vm.drop_caches=3; sudo sync
    sudo mkdir -p \\$HOME/dev
    sudo chown vagrant:vagrant -R ~vagrant
    git clone https://github.com/viasite-ansible/ansible-role-zsh \\$HOME/dev/ansible-role-zsh || true
    sudo apt-get install software-properties-common -y
    sudo apt-add-repository ppa:ansible/ansible -y
    sudo apt-get update
    sudo apt-get install ansible -y
    sudo mkdir -p /etc/ansible/roles
    sudo chown vagrant:vagrant -R /etc/ansible/roles

    sudo curl -fsSL 'https://github.com/heppu/gkill/releases/download/v1.0.2/gkill-linux-amd64' > /usr/local/bin/gkill
    sudo chmod +x /usr/local/bin/gkill
    sudo curl -fsSL 'https://github.com/rgburke/grv/releases/download/v0.3.2/grv_v0.3.2_linux64' > /usr/local/bin/grv
    sudo chmod +x /usr/local/bin/grv
    sudo curl --silent -L 'https://github.com/simeji/jid/releases/download/v0.7.6/jid_linux_amd64.zip' > /usr/local/src/jid.zip
    sudo unzip /usr/local/src/jid.zip -d /usr/local/bin
    sudo chmod +x /usr/local/bin/jid

    sudo curl -fsSL 'https://github.com/sharkdp/fd/releases/download/v7.2.0/fd_7.2.0_amd64.deb' > /usr/local/src/fd_7.2.0_amd64.deb; \
    sudo apt install -y /usr/local/src/fd_7.2.0_amd64.deb

    sudo sed -ri 's/^session\s+required\s+pam_loginuid.so$/session optional pam_loginuid.so/' /etc/pam.d/sshd
    sudo sed -ri 's/^#?PermitRootLogin\s+.*/PermitRootLogin yes/' /etc/ssh/sshd_config
    sudo sed -ri 's/^#?PubkeyAuthentication\s+.*/PubkeyAuthentication yes/' /etc/ssh/sshd_config
    sudo sed -ri 's/requiretty/!requiretty/' /etc/sudoers
    echo 'root:root' | sudo chpasswd

    sudo git clone https://github.com/bossjones/debug-tools /usr/local/src/debug-tools || true
    sudo /usr/local/src/debug-tools/update-bossjones-debug-tools
SCRIPT

# This script to install k8s using kubeadm will get executed after a box is provisioned
$postInstall = <<-SCRIPT
    cat <<EOF >/home/vagrant/run_as_vagrant.sh
#!/usr/bin/env bash

set -x
set -e

export _HOME="~vagrant"

# fnm
curl -fsSL https://github.com/Schniz/fnm/raw/master/.ci/install.sh | bash
export PATH="/home/vagrant/.fnm:$PATH"
# echo 'eval "\\$(fnm env --multi)"' >> \\$HOME/.bashrc
eval "\\$(fnm env --multi)"
fnm install v10
fnm use v10
npm install --global pure-prompt


sudo apt-get install build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev wget unzip -y
sudo apt-get install --no-install-recommends make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev -y
sudo apt-get install -y make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev python-openssl git python-virtualenv

curl -fsSL https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer | bash

echo 'export PYENV_ROOT="\\$HOME/.pyenv"' >> \\$HOME/.bashrc
echo 'export WORKON_HOME="\\$HOME/.pyenv/versions"' >> \\$HOME/.bashrc
echo 'export PROJECT_HOME=\\$HOME/dev' >> \\$HOME/.bashrc
echo 'export PATH="\\$HOME/.pyenv/bin:$PATH"' >> \\$HOME/.bashrc
echo 'eval "\\$(pyenv init -)"' >> \\$HOME/.bashrc
# echo 'eval "\\$(pyenv virtualenv-init -)"' >> \\$HOME/.bashrc

export PYENV_ROOT="\\$HOME/.pyenv"
export WORKON_HOME="\\$HOME/.pyenv/versions"
export PROJECT_HOME=\\$HOME/dev
export PATH="\\$HOME/.pyenv/bin:$PATH"
eval "\\$(pyenv init -)"
eval "\\$(pyenv virtualenv-init -)"

cat \\$HOME/.bashrc

source \\$HOME/.bashrc

pyenv rehash

env PYTHON_CONFIGURE_OPTS="--enable-shared --enable-optimizations --enable-ipv6" PROFILE_TASK="-m test.regrtest --pgo test_array test_base64 test_binascii test_binhex test_binop test_bytes test_c_locale_coercion test_class test_cmath test_codecs test_compile test_complex test_csv test_decimal test_dict test_float test_fstring test_hashlib test_io test_iter test_json test_long test_math test_memoryview test_pickle test_re test_set test_slice test_struct test_threading test_time test_traceback test_unicode" pyenv install 3.7.4

pyenv virtualenv 3.7.4 tools3
pyenv shell tools3
mkdir -p \\$HOME/.bin \\$HOME/.local/bin
pip install --user sqliterepl

pyenv virtualenv 3.7.4 ultron8_venv374
pyenv shell ultron8_venv374
pyenv global ultron8_venv374
pyenv rehash

export RBENV_ROOT=/usr/local/rbenv
sudo mkdir -p /usr/local/rbenv
sudo chmod 777 /usr/local/rbenv
curl -fsSL https://github.com/rbenv/rbenv-installer/raw/master/bin/rbenv-installer | bash

mkdir -p "\\$HOME/.zsh"
git clone https://github.com/sindresorhus/pure.git "\\$HOME/.zsh/pure"

git clone https://github.com/zsh-users/antigen.git \\$HOME/.antigen/antigen

# mkdir -p \\$HOME/.fonts \\$HOME/.config/fontconfig/conf.d \
#   && wget -P \\$HOME/.fonts https://github.com/powerline/powerline/raw/develop/font/PowerlineSymbols.otf \
#   && wget -P \\$HOME/.config/fontconfig/conf.d/ https://github.com/powerline/powerline/raw/develop/font/10-powerline-symbols.conf \
#   && fc-cache -vf \\$HOME/.fonts/

# # # SOURCE: https://github.com/veggiemonk/ansible-dotfiles/blob/master/tasks/fonts.yml
# git clone https://github.com/powerline/fonts \\$HOME/powerlinefonts && \
#   cd \\$HOME/powerlinefonts; \\$HOME/powerlinefonts/install.sh \
#   && fc-cache -f

git clone https://github.com/samoshkin/tmux-config.git \\$HOME/dev/tmux-config
echo "------------------Finished------------------"
echo "Now run ansible-galaxy"
echo 'vagrant:vagrant' | chpasswd

set +x

EOF
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

      vm_config.vm.provision 'shell', privileged: true, inline: $configureBox
      vm_config.vm.provision 'shell', privileged: false, inline: $postInstall

      vm_config.vm.provision :shell, privileged: false, inline: "cat /srv/vagrant_repos/ultron8/vagrant/insecure_ultron8_key.pub >> /home/vagrant/.ssh/authorized_keys"
      vm_config.vm.provision :shell, inline: "install -m 644 /srv/vagrant_repos/ultron8/vagrant/hosts /etc/hosts"
      vm_config.vm.provision :shell, inline: "install -m 755 /srv/vagrant_repos/ultron8/vagrant/sync_code.sh /usr/local/bin/sync_ultron8.sh"
      vm_config.vm.provision :shell, inline: "install -m 755 /srv/vagrant_repos/ultron8/vagrant/sync_code.sh /usr/local/bin/sync_code.sh"
      vm_config.vm.provision :shell, privileged: false, inline: "cd && rsync -r --exclude .vagrant --exclude .git /srv/vagrant_repos/ultron8/ ~/ultron8/ && sudo chown vagrant:vagrant -R ~vagrant && cd ~/ultron8 && ls -lta"
      vm_config.vm.provision :shell, privileged: false, inline: "cd && rsync -r --exclude .vagrant --exclude .git /srv/vagrant_repos/ultron8/vagrant/.zsh* ~/ && sudo chown vagrant:vagrant -R ~vagrant && cd ~/ && ls -lta | grep .zsh"
    end
  end
end
