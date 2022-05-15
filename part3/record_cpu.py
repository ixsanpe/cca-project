import psutil
import time

log = open('cpu_utilization_res.csv', 'w')
log.write('TIME,UTILIZATION\n')
#try:
while True:
    log.write('time'+','+ str(psutil.cpu_percent(interval=1, percpu=False)) +'\n')
    print(psutil.cpu_percent(interval=1, percpu=False))
    time.sleep(5)
#except:
#    log.close()