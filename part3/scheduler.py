import subprocess
import json



def delete_jobs():
    jobs = ["parsec-dedup", "parsec-blackscholes", "parsec-ferret",
            "parsec-freqmine", "parsec-canneal", "parsec-splash2x-fft"]  # get_jobs()

    if len(jobs) == 0:
        print("No previous jobs to delete")
        return

    deleteJobsStatement = "kubectl delete job {}"
    for job in jobs:
        print(f"Deleting job {job}")
        subprocess.run(deleteJobsStatement.format(job).split(" "))

# Clean up - Delete any parsec jobs before starting execution
delete_jobs()

# Schedule jobs
location = ""

vm8jobs = ["parsec-freqmine.yaml", "parsec-fft.yaml", "parsec-canneal.yaml", "parsec-blackscholes.yaml"]
vm4jobs = ["parsec-ferret.yaml", "parsec-dedup.yaml"]

command = "kubectl create -f {}{}"

print("Started scheduling jobs")

# Ferret is a CPU intensive job, so, we allocate 6 CPUs to it.
# Canneal doesn't scale very well, so, we only allocate 2 CPUs to it.
# Canneal and Ferret end around the same time and Dedup scales well up to 4 threads, so, we allocate 4 CPUs to it.
# Schedule VM8
for job in vm8jobs:
    subprocess.run(command.format(location, job).split(" "))

# Freqmine is a CPU intensive task too, so, it cannot be collocated with Ferret.
# Blackscholes and FFT do not intere with each other considerably, so, they are collocated and share equal amounts
# of CPU. FFT is a memory intensive task and VM B has limited RAM. In order to prevent job from crashing, we limit
# the amount of RAM FFT job can use.
# Schedule VM4
for job in vm4jobs:
    subprocess.run(command.format(location, job).split(" "))

print("Completed scheduling jobs")

command = "kubectl get pods"
subprocess.run(command.split(" "))