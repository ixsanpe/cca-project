import docker
import psutil
from time import sleep

#sudo usermod -a -G docker isanchez


def main():



    cpu_util = psutil.cpu_percent(interval=5)
    client = docker.from_env()


