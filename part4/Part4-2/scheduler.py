import time
import sys
from utility import run_parsec_job, delete_jobs, switch_SMALL_LARGE, switch_LARGE_SMALL
import json

from enum import Enum

from utility import *


#################################CODE##############################


# Delete any previous docker stuff
delete_jobs()

# Initialize ---> Run memcached and initial jobs

# Run memcached

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

    ######## Update memcached resource allocation & Status ########

    # Get current stats for memcached.

    # If memcached in SMALL

        # Does it need to go to LARGE

    # If memcached in LARGE

        # Does it need to go to SMALL


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
                        # Move to other container
                        large_core_block_container = small_core_block_container
                        small_core_block_container = None

                        # change Job affinity
                        large_core_block_container.update(cpuset_cpus=large_core_block)
                    else:
                        large_core_block_container = None
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

    # Check if currently running
    
    # If everthing that can be ran in small block has been ran
    if small_core_block_container == None:
        continue

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
                
                # Set lock
                lock_large = True
                # Switch state to large
                if memcached_state == mc_state.SMALL:
                    # TODO:TODO:TODO:TODO: Activate this when mc implemented
                    pass
                    # switch_SMALL_LARGE(memcached_pid)
                # Set small block to empty
                small_core_block_container = None                

            else:
                next_med_job = medium_tasks_queue.pop(0)
                print('    Starting Next Medium job: ' + next_med_job)
                large_core_block_container = run_parsec_job(next_med_job, large_core_block , thread_allocations[next_med_job])


        else:
            # then add job from small queue
            next_short_job = short_tasks_queue.pop(0)
            print('        Starting Next Short job: ' + next_short_job)
            large_core_block_container = run_parsec_job(next_short_job, large_core_block , thread_allocations[next_short_job])                         
 

    else:
        # print('Small core block busy')
        pass

# Print diagnostic information about run





for job in finished_jobs:
    # record remained of job info
    job_info[job.name]['status'] = job.status
    job_info[job.name]['log'] = job.logs()[-log_tail_length]

    print(job.logs()[-log_tail_length])

    print()
    print(job.name + ' -- Status: ' + job.status)
    


print('################## RESULTS ##################')
print(json.dumps(job_info, sort_keys=True, indent=4))
print('Results saved to: ' + results_file)
print('#############################################')


# Save results
with open(results_file,"w") as rf:
    json.dump(job_info,rf)

