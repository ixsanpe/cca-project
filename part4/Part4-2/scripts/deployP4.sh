## Path: ../part4/Part4-2


gsutil mb gs://cca-eth-2022-group-25-2-isanchez/

# deploy.sh
export KOPS_STATE_STORE=gs://cca-eth-2022-group-25-2-isanchez/
export KOPS_FEATURE_FLAGS=AlphaAllowGCE
PROJECT=cca-eth-2022-group-25-2
#`gcloud config get-value project`
kops create -f part4.yaml
kops update cluster part4.k8s.local --yes --admin
kops validate cluster --wait 10m
kubectl get nodes -o wide\


# Install memcached on memcache-server VM

#mem=`kubectl get nodes | grep memcache-server | awk '{print $1}'`

#bash scripts/commands_ssh.sh $mem < scripts/inrstall_memcached.sh