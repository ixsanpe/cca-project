import time
import sys


from enum import Enum


USAGE = 'scheduler.py <memcached_process_id> \
    Memcached PID must be the global pid from /var/memcached.pid not pid of individual thread'

if len(sys.argv) not 2:
    print(USAGE)
    return
else:
    try:
        memcached_pid = int(sys.argv[1])
    except:
        print('ERROR: MEMCACHED PID MUST BE AN INT!')
        print(USAGE)
        return


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
    'fft': 1,
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
long_tasks_queue = ['dedup','splash2x-fft']
short_tasks_queue = ['canneal','blackscholes']
medium_tasks_queue = ['freqmine','ferret']


# CPU Core Blocks ID's and Pointers to Currently Running Containers
memcached_reserved_core = '0'
memcachde_container = None

small_core_block = '1'
small_core_block_container = None

large_core_block = '2,3'
large_core_block_container = None



'''
Memcached State:

Memcached has two possible states governed by a FSM. Large and small. In large it gets 2 cores, in small it gets 1 core.
Moving between states is determined by thresholds for what the Target QPS is.


SMALL --> LARGE: Single core utilization above 50%
LARGE --> SMALL: 

'''

# Memcached state TODO: What should its starts state be?

class mc_state(Enum):
    SMALL = 0
    LARGE = 1


# Motivation: LS is conservative limit meant to prevent violation. 
# SL is less conservative, but the data we gathered makes it hard to pick a better one
# TODO: If we are getting lots of violations, both these limits could be made more conservative

SL_threashold = 50 # Trigger when state SMALL and single core utilization above 50%
LS_threashold = 120 # Trigger when LARGE and two core utilization below 120%

memcached_state = mc_state.SMALL





# Scheduler interval
interval = 1.0

#################################CODE##############################

# Initialize ---> Run memcached and initial jobs

# Run memcached


# Start initial large_block job


# Start initial small_block job



# Main loop of scheduler
while True:
    time.sleep(interval)

    ######## Update memcached resource allocation & Status ########

    # Get current stats for memcached.

    # If memcached in SMALL

        # Does it need to go to LARGE

    # If memcached in LARGE

        # Does it need to go to SMALL


    ######## Update large_core_block jobs #######

    # Check if job currently running

        # If no, then add a job to it

        # Are there more jobs in long job queue?

            # If yes, adda long job

            # If no, look for a medium job

                # If no medium job, look for a small job
                
                # If no small job, try to move from small_block to large_block

                    # If no, we're done!!! 

    ######## Update small_core_block jobs #######


    # Check if currently running

        # If no, then add job from small queue

            # If no job in small queue, chek med queue

            # If no job in med queue give memcached all the core

                # TODO: some kind of flag so we aren;t checking this for no reason
                # Might not be neccesary if enough small/med jobs


    ######## Check if execution of all jobs finished #########

    #TODO: Determine if this step neccesary or if checking this when looking for large jobs is enough



