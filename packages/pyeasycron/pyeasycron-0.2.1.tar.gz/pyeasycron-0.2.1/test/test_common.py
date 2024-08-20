import sys
sys.path.insert(0, '..')
import easycron
import time
from datetime import datetime, timedelta


def func1():
    print(f"in func1: {datetime.now()}")


def func2():
    print(f"in func2: {datetime.now()}")


def func3():
    print(f"in func3: {datetime.now()}")


if __name__ == '__main__':
    easycron.register(func1, interval=timedelta(minutes=3))
    easycron.register(func2, cron_expr='*/2 * * * *')

    easycron.run(block=False)
    time.sleep(300)

    easycron.cancel(func2)
    easycron.register(func3, interval=timedelta(minutes=1))

    time.sleep(300)
