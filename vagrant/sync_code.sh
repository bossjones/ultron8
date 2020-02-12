#!/usr/bin/env bash

cd && rsync -r --exclude .vagrant --exclude .git /vagrant/ ~/ultron8/ && cd ~/ultron8 && ls -lta
