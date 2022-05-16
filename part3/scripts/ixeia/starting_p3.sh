#gsutil mb gs://cca-eth-2022-group-25-2-isanchez/
#bash scripts/ixeia/deploy.sh

# get info we need later:
a=`kubectl get nodes | grep client-agent-a | awk '{print $1}'`
b=`kubectl get nodes | grep client-agent-b | awk '{print $1}'`
m=`kubectl get nodes | grep client-measure | awk '{print $1}'`

# connect to the 3 VMs: 
bash scripts/ixeia/commands_ssh.sh $a < scripts/ixeia/install_mcperf.sh
bash scripts/ixeia/commands_ssh.sh $b < scripts/ixeia/install_mcperf.sh
bash scripts/ixeia/commands_ssh.sh $m < scripts/ixeia/install_mcperf.sh

# install memcache.yaml
bash scripts/ixeia/install_memcache.sh

AGENT_A_INTERNAL_IP=`kubectl get nodes -o wide | grep client-agent-a | awk '{print $6}'`
AGENT_B_INTERNAL_IP=`kubectl get nodes -o wide | grep client-agent-b | awk '{print $6}'`
MEMCACHED_IP=`kubectl get pods -o wide | grep memcached | awk '{print $6}'`