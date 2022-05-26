#! /bin/bash

# In this script we run the static scheduler for part 3.
# The separation of jobs is as follows:
	# 4-core VM: ferret and dedup
	# 8-core VM: freqmine, blackscholes, fft and canneal
	
# The proposed scheduling scheme has four jobs dependencies:
	# 1- dedup after ferret in 4-core VM
	# 2- blackscholes after freqmine in 8-core VM (simultaneously with fft)
	# 3- fft after freqmine in 8-core VM (simultaneously with blackscholes)
	# 4- canneal after blackscholes and consequently freqmine in 8-core VM

# Delete previous jobs and pods:
kubectl delete jobs --field-selector status.successful=1
kubectl delete jobs --field-selector status.successful=0
kubectl delete pods --all

# Run initial jobs: Ferret, Freqmine
kubectl create -f parsec-freqmine.yaml
kubectl create -f parsec-ferret.yaml

echo 'created freqmine and ferret'


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
        echo 'create dedup'
    fi
    # Check for Freqmine ---> BlackScholes	& FFT
    if [ "$freqmine" == "$complete" ]; then
        kubectl create -f parsec-blackscholes.yaml
		kubectl create -f parsec-fft.yaml
        echo 'create blackscholes and fft'
    fi
    # Check for Freqmine & Blackscholes ---> Canneal
    if [ "$freqmine" == "$complete" ] && [ "$blackscholes" == "$complete" ]; then
        kubectl create -f parsec-canneal.yaml
        echo 'create canneal'
    fi
	# Check for end of all jobs to deploy results 
    if [ "$ferret" == "$complete" ] && [ "$freqmine" == "$complete" ] && [ "$fft"=="$complete" ] && [ "$canneal"=="$complete" ] && [ "$dedup"=="$complete" ] && [ "$blackscholes"=="$complete" ]; then
		kubectl get pods -o json > results.json
		python3 get_time.py results1.json
		break
    fi

    sleep 1

done
