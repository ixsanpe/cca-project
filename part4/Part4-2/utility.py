'''
Utility functions for dynamic parsec/memcached scheduler.
'''
import docker
import subprocess
import psutil

util_client = docker.from_env()

#TODO: Put this kinda stuff in a seperate parameters file
class mc_state(Enum):
    SMALL = 0
    LARGE = 1


'''
Handy stuff

# Uses no CPU or memory while stopped. Kills the process inside
container.stop
container.restart


# Pauses/Unpauses container execution
container.pause
container.unpause


'''

################## PARSEC MANAGEMENT FUNCTIONS #######################


def run_parsec_job(jobname, cpuset, n_threads):
    '''
    docker run --cpuset-cpus="0" -d --rm --name parsec \
    anakli/parsec:blackscholes-native-reduced \
    ./bin/parsecmgmt -a run -p blackscholes -i native -n 2


    # Fun fact:
    If you use -d with --rm, the container is removed when it exits or when the daemon exits, whichever happens first.
    '''

    img = 'anakli/parsec:' + jobname + '-native-reduced'

    cmd = './bin/parsecmgmt -a run -p ' + jobname + ' -i native -n ' + str(n_threads)

    cont = util_client.containers.run(
        name = jobname,
        image =  img,
        command = cmd,
        cpuset_cpus = cpuset, # In cpuset format 1-3 /// 1,4,
        detach=True
    )

    # Return container
    return cont


################## MEMCACHED FSM FUNCTIONS #######################

mcsmall_cores = '0'
mclarge_cores = '0,1'

def get_memcached_utilization(mc_state):
    '''
    return sum of utilization of cores memecached is bound to
    '''
    


# SHOWER THOUGHT: This would be nicer with ps.sched_getaffinity, but im not sure how to handle the multiple processes 
# memcached spawns other that with taskset.
# 'taskset -a --pid --cpu-list cpu_id pid'

def switch_SMALL_LARGE(mc_pid):
    '''
    Switch memcached allocation from small to large

    WARNING: Don't forget to switch memcached flag in main
    '''
    cmd = 'taskset -a --pid --cpu-list 0,1 ' + str(mc_pid)
    process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)

    # Instead of waiting for process to terminate, lets just do extensive unit testing to make sure it works :^^^^)
    #output, error = process.communicate()


def switch_LARGE_SMALL(mc_pid):
    '''
    Switch memcached allocation from large to small

    WARNING: Don't forget to switch memcached flag in main
    '''
    cmd = 'taskset -a --pid --cpu-list 0,1 ' + str(mc_pid)
    process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)