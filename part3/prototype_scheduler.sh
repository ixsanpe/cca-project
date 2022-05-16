#! /bin/bash

# Our proposed scheduling scheme has three job dependencies
# 4-core-high-mem:
#   Ferret ---> Dedup 
# 8-core-normal:
#   FFT ---> BlackScholes
#   Freqmine ---> Canneal

# Run initial jobs: Ferret, FFT, Freqmine

#TODO: Are these commands correct? Were we running with any extra parameters?
kubectl create -f parsec-freqmine.yaml
kubectl create -f parsec-ferret.yaml
kubectl create -f parsec-fft.yaml


# At Each tick
while :
do
    # For each dependency check if job completed

    # Record job status
    kubectl get jobs -o wide > temporary_file.raw

    # Check for Ferret ---> Dedup
    if grep temporary_file --quiet <TODO: Regular expression that matches the job completed line>; then
        kubectl create -f parsec-dedup.yaml
    fi
    # Check for FFT ---> BlackScholes
    if grep temporary_file --quiet <TODO: Regular expression that matches the job completed line>; then
        kubectl create -f parsec-blackscholes.yaml
    fi
    # Check for Freqmine ---> Canneal
    if grep temporary_file --quiet <TODO: Regular expression that matches the job completed line>; then
        kubectl create -f parsec-canneal.yaml
    fi

    # TODO: If all jobs completed/ran, quit
        # Or just wait a bit and kill the script with ctrl-c idk

	# TODO: Is this parameter good? Should it be smaller to improve efficiency?
	sleep 1
done
