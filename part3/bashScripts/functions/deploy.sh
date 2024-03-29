export KOPS_STATE_STORE=gs://cca-eth-2022-group-25-2-isanchez/
export KOPS_FEATURE_FLAGS=AlphaAllowGCE
PROJECT=cca-eth-2022-group-25-2
#`gcloud config get-value project`
kops create -f part3.yaml
kops update cluster part3.k8s.local --yes --admin
kops validate cluster --wait 10m
kubectl get nodes -o wide