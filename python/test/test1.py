# -*- coding:utf-8 -*-
import threading
from time import ctime,sleep

def music(func):
    for i in range(6):
        print "I was listening to music %s. %s" % (func,ctime())
        sleep(9)

def movie(func):
    for i in range(8):
        print "I was at the movies %s! %s" % (func,ctime())
        sleep(5)

if __name__ == '__main__':
    threads=[]
    music=threading.Thread(target=music,args=("Roll in deap",))
    threads.append(music)
    movie=threading.Thread(target=movie,args=("Avanda",))
    threads.append(movie)

    for t in threads:
        t.setDaemon(True)
        t.start()

    for t in threads:
        t.join()

    print "all over %s" % ctime()