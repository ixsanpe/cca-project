export KOPS_STATE_STORE=gs://cca-eth-2022-group-25-2-lheath/
export KOPS_FEATURE_FLAGS=AlphaAllowGCE
PROJECT=`gcloud config get-value project`
kops create -f ../part35.yaml

#kops update cluster part35.k8s.local --yes --admin
#kops validate cluster --wait 10m
#kubectl get nodes -o wide

