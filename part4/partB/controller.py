import docker
import psutil
from time import sleep

# Command window: use the SDK programmatically without using sudo
#sudo usermod -a -G docker isanchez


def main():

    image = ('parsec \ anakli/parsec:', '-native-reduced \ ./bin/parsecmgmt')
    blackscholes = ('blackscholes')

    while(True):
        cpu_util = psutil.cpu_percent(interval=5)
        nCPUs = "0"
  


