import time
import sys
from utility import run_parsec_job, delete_jobs, switch_SMALL_LARGE, switch_LARGE_SMALL
import json

from enum import Enum

from utility import *


USAGE = 'scheduler.py <memcached_process_id> \
    Memcached PID must be the global pid from /var/memcached.pid not pid of individual thread'

if len(sys.argv) != 2:
    print(USAGE)
    quit()
else:
    try:
        memcached_pid = int(sys.argv[1])
    except:
        print('ERROR: MEMCACHED PID MUST BE AN INT!')
        print(USAGE)
        quit()



#################################CODE##############################


# Delete any previous docker stuff
delete_jobs()

# Initialize ---> Run memcached and initial jobs


# Record start time
job_info['global']['start'] = datetime.timestamp(datetime.now())



# A juicy alternative to reading the docker documentation
sbc_paused = False

# Run memcached

# Set initial mc state
print('Setting MC to Initial State')
switch_LARGE_SMALL(memcached_pid)

# Start initial large_block job
next_large_job = long_tasks_queue.pop(0)
large_core_block_container = run_parsec_job(next_large_job, large_core_block , thread_allocations[next_large_job])
print('Starting First Long Job in Large Block: ' + next_large_job)

# Start initial small_block job
# Note we are starting memcached in large mode just in case, so this container is instantly paused
next_small_job = short_tasks_queue.pop(0)
small_core_block_container = run_parsec_job(next_small_job, small_core_block , thread_allocations[next_small_job])
print('Starting First Short Job in Small Block: ' + next_small_job)


# Main loop of scheduler
while True:
    time.sleep(interval)

    ######## Update memcached FSM ########

    # Get current stats for memcached.
    current_util = get_memcached_utilization(memcached_state)
    
    # If memcached in SMALL
    if lock_large:
        # Memcached in LARGE and no longer allowed to change
        pass
    elif memcached_state == mc_state.SMALL :
        # Does it need to go to LARGE
        small_core_block_container.reload()
        if small_core_block_container.status == 'paused':
            try:
                small_core_block_container.unpause()
            except:
                pass
        if current_util >= SL_threashold:
            
            # Unpause the job
            small_core_block_container.reload()
            if small_core_block_container != None and small_core_block_container.status == 'paused':
                # Log the changes
                sbc_paused = False
                job_info[small_core_block_container.name]['timestamps'].append(datetime.timestamp(datetime.now()))
                try:
                    small_core_block_container.unpause()
                except:
                    pass
            
            print('Updating memcached from SMALL to LARGE')
            switch_SMALL_LARGE(memcached_pid)
            memcached_state = mc_state.LARGE

    else: # memcached_state == mc_state.LARGE
        # Does it need to go to SMALL
        if current_util <= LS_threashold:
            # If job in small, pause job
            large_core_block_container.reload()
            if small_core_block_container != None and small_core_block_container.status != 'exited':
                # Log the change
                sbc_paused = True
                job_info[small_core_block_container.name]['timestamps'].append(datetime.timestamp(datetime.now()))
                try:
                    small_core_block_container.pause()
                except:
                    pass

            print('Updating memcached from LARGE to SMALL')
            switch_LARGE_SMALL(memcached_pid)
            memcached_state = mc_state.SMALL
   

    ######## Update large_core_block jobs #######

    # Check if job currently running
    large_core_block_container.reload()

    if large_core_block_container.status == 'exited':
        # pause container and add to finished jobs
        retire_job(large_core_block_container)
        # this should make errors easier to spot
        large_core_block_container = None


        # If no, then add a job to it
        print('Large core block empty')

        # Are there more jobs in long job queue?i
        if long_tasks_queue == []:
            print('Long Queue Empty')
            # If no, look for a medium job
            if medium_tasks_queue == []:
                print('    Medium Queue Empty')
                # If no medium job, look for a small job
                if short_tasks_queue == []:
                    print('        Short Queue Empty')
                    # If no small job, try to move from small_block to large_block
                    if small_core_block_container != None:
                        print('            Moving Job From Small to Large Block')

                        # If neccesary unpause 
                        if sbc_paused:
                            job_info[small_core_block_container.name]['timestamps'].append(datetime.timestamp(datetime.now()))
                            try:
                                small_core_block_container.unpause()
                            except:
                                pass
                            sbc_paused = False

                        # Short no longer doing stuff
                        lock_large = True
                        if memcached_state == mc_state.SMALL:
                            print('Permanently Switching to Large')
                            switch_SMALL_LARGE(memcached_pid)


                        # Move to other container
                        large_core_block_container = small_core_block_container
                        small_core_block_container = None

                        # change Job affinity
                        large_core_block_container.update(cpuset_cpus=large_core_block)
                    else:
                        large_core_block_container = None

                        # Give memcached enough cores just in case TODO: Determine if this is really necessary
                        switch_SMALL_LARGE(memcached_pid)

                        # If no, we're done!!!
                        print('No jobs in long, med, short quques/ Large, small core blocks!!!')
                        print('---All PARSEC JOBS COMPLETED---')
                        print('Done.')
                        break
                else:
                    next_short_job = short_tasks_queue.pop(0)
                    print('        Starting Next Short job: ' + next_short_job)
                    large_core_block_container = run_parsec_job(next_short_job, large_core_block , thread_allocations[next_short_job])                         
            else:
                # add a medium job
                next_med_job = medium_tasks_queue.pop(0)
                print('    Starting Next Medium job: ' + next_med_job)
                large_core_block_container = run_parsec_job(next_med_job, large_core_block , thread_allocations[next_med_job])
        else:
            # If yes, adda long job
            next_long_job = long_tasks_queue.pop(0)
            print('    Starting Next long job: ' + next_long_job)
            large_core_block_container = run_parsec_job(next_long_job, large_core_block , thread_allocations[next_long_job])

    else:
        # print('Large core block busy')
        pass

    ######## Update small_core_block jobs #######

    # If small container ran out of tasks, it has been permanently assigned to memcahced so we can ignore it
    if lock_large:
        continue

    # Check if currently running
    small_core_block_container.reload()
    if small_core_block_container.status == 'exited':

        # pause container and add to finished jobs
        retire_job(small_core_block_container)
        # this should make errors easier to spot
        small_core_block_container = None

        print('Small core block empty')

        # check if job in small queue
        if short_tasks_queue == []:
            # If no job in small queue, chek med queue
            print('Short Queue Empty')
            if medium_tasks_queue == []:
                print('    Medium Queue Empty')
                # If no job in med queue give memcached all the core
                print('    Giving Memcached all small core block resources')
                
                # Switch state to large
                if memcached_state == mc_state.SMALL:
                    switch_SMALL_LARGE(memcached_pid)
                
                # Set lock
                lock_large = True
                small_core_block_container = None                


            else:
                next_med_job = medium_tasks_queue.pop(0)
                print('    Starting Next Medium job: ' + next_med_job)
                small_core_block_container = run_parsec_job(next_med_job, large_core_block , thread_allocations[next_med_job])
        else:
            # then add job from small queue
            next_short_job = short_tasks_queue.pop(0)
            print('        Starting Next Short job: ' + next_short_job)
            small_core_block_container = run_parsec_job(next_short_job, large_core_block , thread_allocations[next_short_job])                         

    else:
        # print('Small core block busy')
        pass


# Record end time

job_info['global']['end'] = datetime.timestamp(datetime.now())


# Print diagnostic information about run

for job in finished_jobs:
    # record remained of job info
    job_info[job.name]['status'] = job.status
    job_info[job.name]['log'] = str(job.logs()[-log_tail_length:-1]).replace('\'', '') # [-log_tail_length]

    #print(job.logs()[-log_tail_length])

    print()
    print(job.name + ' -- Status: ' + job.status)
    


print('################## RESULTS ##################')
print(job_info)
print(json.dumps(job_info, sort_keys=True, indent=4))
print('Results saved to: ' + results_file)
print('#############################################')


# Save results
with open(results_file,"w") as rf:
    json.dump(job_info,rf)

