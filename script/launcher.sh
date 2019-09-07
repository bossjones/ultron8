#!/usr/bin/env bash

# SOURCE: https://git.corp.adobe.com/AAM/qe-env/blob/11626148e7b10c316bf6514ca24af88c32984090/docker/launcher.sh

SSHAGENT=/usr/bin/ssh-agent
SSHAGENTARGS="-s"
eval $($SSHAGENT $SSHAGENTARGS)
trap "kill $SSH_AGENT_PID" 0

setup_ssh_agent() {
  SSHAGENT=/usr/bin/ssh-agent
  SSHAGENTARGS="-s"
  eval $($SSHAGENT $SSHAGENTARGS)
  ssh-add ~/.ssh/id_rsa
  trap "kill $SSH_AGENT_PID" 0
}

main() {
  setup_ssh_agent

  $@
}

main $@
