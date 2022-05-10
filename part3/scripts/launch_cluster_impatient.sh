export KOPS_STATE_STORE=gs://cca-eth-2022-group-25-impatient-lheath-2/
export KOPS_FEATURE_FLAGS=AlphaAllowGCE
PROJECT=`gcloud config get-value project`
kops create -f ../part_3_impatient.yaml

kops update cluster part3i.k8s.local --yes --admin
kops validate cluster --wait 10m
kubectl get nodes -o wide

