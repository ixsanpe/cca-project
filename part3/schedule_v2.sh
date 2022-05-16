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
	
	ferret=`kubectl get jobs -o wide | grep parsec-ferret | awk '{print $2}'`
	freqmine=`kubectl get jobs -o wide | grep parsec-freqmine | awk '{print $2}'`
	fft=`kubectl get jobs -o wide | grep parsec-splash2x-fft | awk '{print $2}'`
	blackscholes=`kubectl get jobs -o wide | grep parsec-blackscholes | awk '{print $2}'`
	dedup=`kubectl get jobs -o wide | grep parsec-dedup | awk '{print $2}'`
	canneal=`kubectl get jobs -o wide | grep parsec-canneal | awk '{print $2}'`
	
	incomplete="0/1"
	complete="1/1"

    # Check for Ferret ---> Dedup
    if [ "$ferret" == "$complete" ]; then
        kubectl create -f parsec-dedup.yaml
    fi
    # Check for FFT ---> BlackScholes	#if [ "$freqmine" == "$complete" ] && [ "$fft" == "$complete" ]; then
    if [ "$freqmine" == "$complete" ]; then
        kubectl create -f parsec-blackscholes.yaml
    fi
    # Check for Freqmine ---> Canneal
    if [ "$freqmine" == "$complete" ]; then
        kubectl create -f parsec-canneal.yaml
    fi
	
    if [ "$ferret" == "$complete" ] && [ "$freqmine" == "$complete" ] && [ "$fft"=="$complete" ] && [ "$canneal"=="$complete" ] && [ "$dedup"=="$complete" ] && [ "$blackscholes"=="$complete" ]; then
		kubectl get pods -o json > results1.json
		python3 get_time.py results1.json
		break
	fi

	sleep 1
	
done 