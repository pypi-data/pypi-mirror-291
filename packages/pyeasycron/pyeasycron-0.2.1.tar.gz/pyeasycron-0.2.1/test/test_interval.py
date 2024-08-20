import sys
sys.path.insert(0, '..')
import easycron
from datetime import datetime


@easycron.every(minutes=1)
def func1():
    print(f"in func1: {datetime.now()}")


@easycron.every(minutes=2)
def func2():
    print(f"in func2: {datetime.now()}")


print(easycron.get_intvinfo())

easycron.run()
