import sys

LongString = '''
Measuring programming progress by lines of code
is like measuring aircraft building progress by weight
-By Bill Gates
If you cannot fly, then run. If you cannot run, then walk. 
And if you cannot walk, then crawl, but whatever you do, you have to keep moving forward.
- By Martin Luter King Jr.
'''

def Hello():
    print("############################")
    SystemInfo()
    print('YCPython.YCFunction.Hello()', __name__)
    print("############################", end='\n\n')

import ctypes
def ListToArray(_li): ## python list to c array
    iList = [x for x in _li if isinstance(x, int)]
    fList = [x for x in _li if isinstance(x, float)]
    if len(_li) == len(iList):
        arr = (ctypes.c_int * len(_li))(*_li)
        return arr
    elif len(_li) == len(fList):
        arr = (ctypes.c_float * len(_li))(*_li)
        return arr
    elif len(_li) == len(iList) + len(fList):
        _lii = [float(x) for x in _li]
        arr = (ctypes.c_float * len(_lii))(*_lii)
        return arr
    else:
        ErrorMessage("I don't know input type")
        pass

# BEGIN ########################################
import inspect
def Message(_msg):
    print(f"{inspect.stack()[1][1]}:{inspect.currentframe().f_back.f_lineno} ", _msg)
def ErrorMessage(_msg):
    sys.stderr.write(f"ERROR: {inspect.stack()[1][1]}:{inspect.currentframe().f_back.f_lineno} " +  _msg + '\n')
# END ##########################################

# BEGIN Decorate ########################################
from time import time
def YCRunTime(func): ## decorate
    def PrintRunTime(*args, **kwargs):
        t0 = time()
        res = func(*args, **kwargs)
        t1 = time()
        print(f"### RunTime {t1-t0}", end=' seconds \n')
        return res
    return PrintRunTime

@YCRunTime
def LongTime():
    sum = 0
    for i in range(101):
        sum += i
    return sum
# END Decorate ########################################

# BEGIN Closure ########################################
def OuterFunc(x):
    xOut = x
    def InnerFunc(y):
        return xOut + y
    return InnerFunc
    
# END Closure ########################################


def Args(*args, **kwargs):
    for arg in args:
        print("arg:" , arg)
    for key, value in kwargs.items():
        print("kwargs:", key,'=', value)

import sys
def SystemInfo():
    print(sys.path)

if __name__ == '__main__':
    Hello()
    li = list(range(0,100))
    arr = ListToArray(li)
    print(type(arr))

    runTime = LongTime()
    print(f"Result {runTime}")

    Args(1, [2, 3], a=1, b='b')

    print(LongString)

    inner = OuterFunc(10)
    inner1 = inner(1)
    inner2 = inner(2)
    inner3 = inner(3)
    print(inner1, inner2, inner3)

    Hello()
