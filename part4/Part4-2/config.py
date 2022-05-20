import time
import sys

from enum import Enum



'''
Allocation:

Long tasks get preference for 2 Core uninterupted cpu block
Short tasks get preference for 1 Core interupted cpu block
Medium tasks go where there is space, preferably on 2 core block if possible
If 2 core block is empty and one core block isnt, move task to 2 core block


Justification for thread allcations is ojn the google docs
'''

# T ---> number of threads
# C ---> depends on witch block they are run on
thread_allocations = {
    'dedup': 1,
    'blackscholes': 2,
    'ferret': 4,
    'freqmine':4 ,
    'canneal':1 ,
    'splash2x-fft': 1,
}

# Store info about job runs incl: Start time, end time, status and tail of 
# log (to check sucesfull completion)


log_tail_length = 6 # In chars

job_info = {
    'global' : {
        'timestamps' : 'Not Available',
        'start' : None,
        'stop' : None,
        'end' : 'Not Available',
        'log' : 'Not Available'
    },
    'dedup': {
        'timestamps' : [],
        'start' : None,
        'end' : None,
        'status' : None,
        'log' : None
    },
    'blackscholes': {
        'timestamps' : [],
        'start' : None,
        'end' : None,
        'status' : None,
        'log' : None
    },
    'ferret': {
        'timestamps' : [],
        'start' : None,
        'end' : None,
        'status' : None,
        'log' : None
    },
    'freqmine': {
        'timestamps' : [],
        'start' : None,
        'end' : None,
        'status' : None,
        'log' : None
    },
    'canneal': {
        'timestamps' : [],
        'start' : None,
        'end' : None,
        'status' : None,
        'log' : None
    },
    'splash2x-fft': {
        'timestamps' : [],
        'start' : None,
        'end' : None,
        'status' : None,
        'log' : None
    },

}




'''
Postioning:

Dedup goes first so that there is no chance it ends up on 2 core block (it is unlikely to benefit from it)

Freqmine and ferret have similar interference profgiles for 
relevant resources so it doesnt really matter witch one is colocated.

Core Blocks:

We have a large core block fo 2 cores that allways runs parsec, 1 block fo 1 core that allways runs memcached
And a small_core_block of 1 core that flip flops between the two are required by memcached. 

Jobs cannot run between core blocks and are isolated to SPECIFIC cpu cores that make up each block
'''


# Task Queues
short_tasks_queue = ['splash2x-fft','dedup']
medium_tasks_queue = ['canneal','blackscholes']
long_tasks_queue = ['freqmine','ferret']


# Might want to change above to smaller set for testing purposes


# CPU Core Blocks ID's and Pointers to Currently Running Containers
memcached_reserved_core = '0'
memcached_container = None

small_core_block = '1'
small_core_block_container = None

large_core_block = '2,3'
large_core_block_container = None


mcsmall_cores = '0'
mclarge_cores = '0,1'


'''
Memcached State:

Memcached has two possible states governed by a FSM. Large and small. In large it gets 2 cores, in small it gets 1 core.
Moving between states is determined by thresholds for what the Target QPS is.


SMALL --> LARGE: Single core utilization above 50%
LARGE --> SMALL: 

'''

class mc_state(Enum):
    SMALL = 0
    LARGE = 1


# Motivation: LS is conservative limit meant to prevent violation. 
# SL is less conservative, but the data we gathered makes it hard to pick a better one
# TODO: If we are getting lots of violations, both these limits could be made more conservative

SL_threashold = 60 # Trigger when state SMALL and single core utilization above 50%
LS_threashold = 130 # Trigger when LARGE and two core utilization below 120%

memcached_state = mc_state.SMALL

# If true, memcached will never go from LARGE to SMALL state
lock_large = False


# Scheduler interval
interval = 1.0
finished_jobs = []


# File path to store results of run
results_file = "run_log.json"



