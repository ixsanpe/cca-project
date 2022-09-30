cd memcache-perf
./mcperf -s 100.96.5.4 --loadonly
./mcperf -s 100.96.5.4 -a 10.156.0.61 -a 10.156.0.58 --noload -T 6 -C 4 -D 4 -Q 1000 -c 4 -t 20 --scan 30000:30500:10