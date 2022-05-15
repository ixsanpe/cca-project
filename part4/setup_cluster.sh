# Set up
export KOPS_STATE_STORE=gs://cca-eth-25-solo/
PROJECT='gcloud config get-value project'
export KOPS_FEATURE_FLAGS=AlphaAllowGCE # to unlock the GCE features
kops create -f part4-louis.yaml

# Deploy
kops update cluster --name part4.k8s.local --yes --admin

# Validate
kops validate cluster --wait 10m


# Check if nodes up
kubectl get nodes -o wide
