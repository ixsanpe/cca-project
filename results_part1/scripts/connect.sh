if [ $# -eq 0 ]
  then
    echo "No arguments supplied. Argument should be of form parsec-server-XXXX"
  else
  gcloud compute ssh --ssh-key-file ~/.ssh/cloud-computing ubuntu@$1 --zone europe-west3-a
fi