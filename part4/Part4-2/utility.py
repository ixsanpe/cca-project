'''
Utility functions for dynamic parsec/memcached scheduler.
'''
import docker
import subprocess
import psutil
from enum import Enum

from config import *

from datetime import datetime

util_client = docker.from_env()

#TODO: Put this kinda stuff in a seperate parameters file
class mc_state(Enum):
    SMALL = 0
    LARGE = 1


'''
Clean up all old parsec jobs
'''

def delete_jobs():
    # Lazy strats for a lazy guy

    # Stop all containers
    subprocess.run("docker kill $(docker ps -q)".split(" "))

    # Delete all containers
    subprocess.run("docker container prune".split(" "))


'''
Handy stuff

# Uses no CPU or memory while stopped. Kills the process inside
container.stop
container.restart


# Pauses/Unpauses container execution
container.pause
container.unpause


# containers have to be reloaded before their status is updated. 
# If finished it should be 'exited'
container.reload()
container.status


'''

################## PARSEC MANAGEMENT FUNCTIONS #######################


def run_parsec_job(jobname, cpuset, n_threads, simlarge=True):
    '''
    docker run --cpuset-cpus="0" -d --rm --name parsec \
    anakli/parsec:blackscholes-native-reduced \
    ./bin/parsecmgmt -a run -p blackscholes -i native -n 2


    # Fun fact:
    If you use -d with --rm, the container is removed when it exits or when the daemon exits, whichever happens first.
    '''
    # print('--------------' + 'Starting ' + jobname + '---------------')

    if simlarge and jobname not in ['dedup', 'blackscholes']:
        img = 'anakli/parsec:simlarge'
        cmd = './bin/parsecmgmt -a run -p ' + jobname + ' -i simlarge -n ' + str(n_threads)
        if jobname == 'splash2x-fft':
            cmd = './bin/parsecmgmt -a run -p splash2x.fft -i simlarge -n ' + str(n_threads)
        
    else:
        img = 'anakli/parsec:' + jobname + '-native-reduced'
        cmd = './bin/parsecmgmt -a run -p ' + jobname + ' -i native -n ' + str(n_threads)
        if jobname == 'splash2x-fft':
            cmd = './bin/parsecmgmt -a run -p splash2x.fft -i native -n ' + str(n_threads)

    cont = util_client.containers.run(
        name = jobname,
        image =  img,
        command = cmd,
        cpuset_cpus = cpuset, # In cpuset format 1-3 /// 1,4,
        detach=True
        #auto_remove=True
    )

    # Log time
    job_info[jobname]['start'] = datetime.now().strftime("%H:%M:%S")
    job_info[jobname]['timestamps'].append(datetime.timestamp(datetime.now()))
    # return container
    return cont


def retire_job(job_container):

        # Log end time 
        job_info[job_container.name]['end'] = datetime.now().strftime("%H:%M:%S")
        job_info[job_container.name]['timestamps'].append(datetime.timestamp(datetime.now()))
        finished_jobs.append(job_container)
        


################## MEMCACHED FSM FUNCTIONS #######################

def get_memcached_utilization(curr_state):
    '''
    return sum of utilization of cores memecached is bound to
    '''

    per_core_usage = psutil.cpu_percent(interval=1, percpu=True)

    if curr_state == mc_state.SMALL:
        return per_core_usage[0]
    else: #curr_state is LARGE
        return per_core_usage[0] + per_core_usage[1]
    


# SHOWER THOUGHT: This would be nicer with ps.sched_getaffinity, but im not sure how to handle the multiple processes 
# memcached spawns other that with taskset.
# 'taskset -a --pid --cpu-list cpu_id pid'

def switch_SMALL_LARGE(mc_pid):
    '''
    Switch memcached allocation from small to large

    WARNING: Don't forget to switch memcached flag in main
    '''
    cmd = 'taskset -a --pid --cpu-list ' +  mclarge_cores + ' ' + str(mc_pid)
    process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)

    # Instead of waiting for process to terminate, lets just do extensive unit testing to make sure it works :^^^^)
    #output, error = process.communicate()


def switch_LARGE_SMALL(mc_pid):
    '''
    Switch memcached allocation from large to small

    WARNING: Don't forget to switch memcached flag in main
    '''
    cmd = 'taskset -a --pid --cpu-list '+ mcsmall_cores + ' ' + str(mc_pid)
    process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)