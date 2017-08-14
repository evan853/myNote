
def decorator(func):
    def inner(*args,**kwargs):
        #print "I'm decorator"
        #print args,kwargs
        argsL=list(args)
        for i in range(len(argsL)):
            if argsL[i]>0:
                argsL[i]=100
        for k in kwargs.keys():
            if kwargs[k]>0:
                kwargs[k]=30
        return func(*argsL,**kwargs)
    return inner

@decorator
def a(x):
    print x

@decorator
def b(x,y=300):
    print x,y


if __name__ == "__main__":
    a(10)
    b(20,y=100)