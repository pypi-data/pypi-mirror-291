import easycron
from datetime import datetime


@easycron.cron('* * * * *')
def func1():
    print(f"in func1: {datetime.now()}")


@easycron.cron('*/2 * * * *')
def func2():
    print(f"in func2: {datetime.now()}")


print(easycron.get_croninfo())

easycron.run()
