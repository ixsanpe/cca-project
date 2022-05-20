#!/bin/bash
a=`kubectl get nodes | grep client-agent | awk '{print $1}'`
m=`kubectl get nodes | grep client-measure | awk '{print $1}'`

bash scripts/commands_ssh.sh $a < scripts/install_mcperf.sh
bash scripts/commands_ssh.sh $m < scripts/install_mcperf.sh