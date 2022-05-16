#! /bin/bash

# Delete previous jobs:
kubectl delete jobs --field-selector status.successful=1
kubectl delete jobs --field-selector status.successful=0
# Our proposed scheduling scheme has three job dependencies
# 4-core-high-mem:
#   Ferret ---> Dedup 
# 8-core-normal:
#   FFT ---> BlackScholes
#   Freqmine ---> Canneal

# Run initial jobs: Ferret, FFT, Freqmine
kubectl create -f parsec-freqmine.yaml
kubectl create -f parsec-ferret.yaml
kubectl create -f parsec-fft.yaml


# At Each tick
while true
do
    # For each dependency check if job completed

    # Record job status
    kubectl get jobs -o wide > temporary_file.raw
	
	ferret=`kubectl get pods -o wide | grep parsec-ferret | awk '{print $3}'`
	freqmine=`kubectl get pods -o wide | grep parsec-freqmine | awk '{print $3}'`
	fft=`kubectl get pods -o wide | grep parsec-splash2x-fft | awk '{print $3}'`
	blackscholes=`kubectl get pods -o wide | grep parsec-blackscholes | awk '{print $3}'`
	dedup=`kubectl get pods -o wide | grep parsec-dedup | awk '{print $3}'`
	canneal=`kubectl get pods -o wide | grep parsec-canneal | awk '{print $3}'`
	
	incomplete="0/1"
	complete="Completed"
	echo "eooe"
	echo "$fft"
    # Check for Ferret ---> Dedup
    if [ "$ferret" == "$complete" ]; then
        kubectl create -f parsec-dedup.yaml
    fi
    # Check for FFT ---> BlackScholes
	#if [ "$freqmine" == "$complete" ] && [ "$fft"=="$complete" ]; then
	if [ "$fft" == "$complete" ]; then 
		echo "hola"
        kubectl create -f parsec-blackscholes.yaml
    fi
    # Check for Freqmine ---> Canneal
    if [ "$freqmine" == "$complete" ]; then
        kubectl create -f parsec-canneal.yaml
    fi
	
	if [ "$ferret" == "$complete" ] && [ "$freqmine" == "$complete" ] && [ "$fft"=="$complete" ] && [ "$canneal"=="$complete" ] && [ "$dedup"=="$complete" ] && [ "$blackscholes"=="$complete" ]; then
		#kubectl get pods -o json > resultsNew.json
		#python3 get_time.py resultsNew.json
		break
	fi
    # TODO: If all jobs completed/ran, quit
        # Or just wait a bit and kill the script with ctrl-c idk

	# TODO: Is this parameter good? Should it be smaller to improve efficiency?
	sleep 1
	
done 