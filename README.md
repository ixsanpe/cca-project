# Cloud Computing Architecture project Spring Semester 2022 @ ETH Zürich
This repository icnludes the code, results and reports for Cloud Computing Architecture course project at ETH Zürich. \
The objective of the project is to schedule latency-sensitive and batch applications in a cloud cluster. It consists of four parts: 
 * **Part 1:** Run a latency-critical application (memcached) inside a container and measure its performance with the metric of tail latency (e.g., 95th percentile latency)
under a desired query rate. Also compare it with different sources of interference. 
* **Part 2:** Deploy six different throughput-oriented workloads from the PARSEC benchmark suite. Explore each workload's sensitivity to resource interference on a small 2 core
and investigate how each workload benefits from parallelism by varying the number of threads on a large 8 core VM without interference. 
* **Part 3:** Static scheduler of the latency critical memcached application from Part 1 and all six batch applications from Part 2. Done in a heterogeneous cluster of VMS with
different number of cores. The scheduling policy aims to minimize the time it takes for all six batch workloads to complete while guaranteeing a tail latency.
* **Part 4:** Dynamic scheduler of the PARSEC jobs on a single 4-core server running memcached. Vary the load on the long-running memcached service, such that the number of cores
needed by the memcached server to meet the tail latency service level objective (SLO) ranges from 1 to 2 cores.
