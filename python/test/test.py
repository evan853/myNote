'''print "A"

class E():
    print "B"
    def __init__(self,name):
        print "C"
        self.name=name
    print "D"

print "F"
name = E("name1")
name = E("name2")'''


#i="global"
'''def tt():
    def inner():
        i="inner"
        print i
#    i="func"
    inner()
#    print i
tt()
#print i'''

import time

def timeit(func):
    def wraper():
        start = time.clock()
        func()
        end = time.clock()
        print end-start
    return wraper

@timeit
def foo():
    print "i am foo()"
foo()
