Running Tron under Vagrant
--------------------------

A Vagrantfile is present that will fire up a working multi-node Tron playground
environment. SOURCE - https://github.com/Yelp/Tron/pull/356/files

Fire this up with::

    $ vagrant up
    $ vagrant ssh master.tron-v

:command:`trond` will be running, with no nodes configured.

A basic environment can then be loaded with :command:`tronfig`::

    ssh_options:
        agent: true

    nodes:
        - name: 'batch-01'
          hostname: 'batch-01'
          username: 'vagrant'
        - name: 'batch-02'
          hostname: 'batch-02'
          username: 'vagrant'
        - name: 'batch-03'
          hostname: 'batch-03'
          username: 'vagrant'

    node_pools:
       - name: all_nodes
         nodes:
         - 'batch-01'
         - 'batch-02'
         - 'batch-03'

    command_context:

    jobs:
        - name: "get_uname_details"
          node: all_nodes
          schedule: "interval 1 minute"
          actions:
          - name: "uname"
            command: "uname -a"

    services:

The tests detailed below should also be runnable in this environment.
