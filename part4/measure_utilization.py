import psutil
import time
from datetime import datetime


log = open('utilization.log', 'w')
log.write('TIME,C1,C2,C3,C4,Total,TimeStamp\n')


while True:
    time.sleep(1)

    dt = datetime.now()
    res = psutil.cpu_percent(interval=None, percpu=True)
    per_core = str(res)[1:-1]
    total = str(sum(res))
    timestamp = str(datetime.timestamp(dt))
    dt = str(dt)
    line = dt + ',' + per_core + ',' + total + ',' + timestamp + '\n'    
    print(line)
    log.write(line)
