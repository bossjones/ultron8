#!/usr/bin/env bash

cd && rsync -r --exclude .vagrant --exclude .git /srv/vagrant_repos/ultron8/ ~/ultron8/ && cd ~/ultron8 && ls -lta
