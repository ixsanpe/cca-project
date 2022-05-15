./mcperf -s INTERNAL_MEMCACHED_IP --loadonly
./mcperf -s INTERNAL_MEMCACHED_IP -a INTERNAL_AGENT_IP \
--noload -T 16 -C 4 -D 4 -Q 1000 -c 4 -t 5 \
--scan 5000:120000:5000

