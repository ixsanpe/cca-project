#! /bin/bash


ferret=`kubectl get pods -o wide | grep parsec-freqmine | awk '{print $3}'`
incomplete="0/1"
complete="Completed"
#echo $ferret
#echo $complete
if [ "$ferret" == "$complete" ]; then
	echo $ferret
fi 