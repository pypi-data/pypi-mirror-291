import sys
sys.path.insert(0, '..')
import easycron
from datetime import datetime
import time


@easycron.cron('*/3 * * * *')
@easycron.cron('*/2 * * * *')
def func3():
    time.sleep(3)
    print(f"in func3: {datetime.now()}")


@easycron.every(minutes=2)
@easycron.cron('*/5 * * * *')
def func2():
    time.sleep(2)
    print(f"in func2: {datetime.now()}")


@easycron.every(minutes=2)
@easycron.every(minutes=1)
def func1():
    time.sleep(1)
    print(f"in func1: {datetime.now()}")


print(easycron.get_croninfo())
print(easycron.get_intvinfo())

easycron.run(concurrency=True)
