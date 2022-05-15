from time import sleep
import psutil

cpu_util = psutil.cpu_percent(interval=5)
