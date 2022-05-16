#! /bin/bash


ferret=`kubectl get jobs -o wide | grep parsec-ferret | awk '{print $2}'`
incomplete="0/1"
complete="1/1"

if [ "$ferret" == "$incomplete" ]; then
	echo $ferret
fi 