#! /bin/bash


# Delete previous jobs:
kubectl delete jobs --field-selector status.successful=1
kubectl delete jobs --field-selector status.successful=0

# create all Kubernetes jobs 
for job in freqmine fft canneal blackscholes ferret dedup; do
	kubectl create -f parsec-${job}.yaml
done

#for job in freqmine fft canneal blackscholes ferret dedup; do
#	parsec_job=parsec-${job}
#	kubectl wait --for=condition=complete job/${parsec_job}
#done
