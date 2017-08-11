# -*- coding:utf-8 -*-
from random import randint

#bubble_sort
def bubble_sort(list):
    length=len(list)
    for index in range(length):
        for i in range(1,length-index):
            if list[i-1]<list[i]:
                list[i],list[i-1]=list[i-1],list[i]
    return list

#selection_sort
def select_sort(list):
    length=len(list)
    for index in range(length):
        for i in range(index,length):
            if list[index]<list[i]:
                list[index],list[i]=list[i],list[index]
    return list

#insertion_sort
def insert_sort(lists):
    # 插入排序
    count = len(lists)
    for i in range(1, count):
        key = lists[i]
        j = i - 1
        while j >= 0:
            if lists[j] > key:
                lists[j + 1] = lists[j]
                lists[j] = key
            j -= 1
    return lists

#shell_sort
def shell_sort(list):
    length=len(list)
    dist=length/2
    while dist>0:
        for i in range(dist,length):
            temp=list[i]
            j=i
            while j>=dist and temp<list[j-dist]:
                list[j]=list[j-dist]
                j-=dist
            list[j]=temp
        dist/=2
    return list

#merge_sort
def merge_sort(list1,list2):
    length_list1=len(list1)
    length_list2=len(list2)
    list3=[]
    j=0
    for i in range(length_list1):
        while list2[j]<list1[i] and j<length_list2:
            list3.append(list2[j])
            j=j+1
        list3.append(list1[i])
    if j<(length_list2-1):
        for k in range(j+1,length_list2):
            list3.append(list2[k])
    return list3

#kp
def kp(arr, i, j):  # 快排总函数
    # 制定从哪开始快排
    if i < j:
        base = kpgc(arr, i, j)
        kp(arr, i, base)
        kp(arr, base + 1, j)

def kpgc(arr, i, j):  # 快排排序过程
    base = arr[i]
    while i < j:
        while i < j and arr[j] >= base:
            j -= 1
        while i < j and arr[j] < base:
            arr[i] = arr[j]
            i += 1
            arr[j] = arr[i]
        arr[i] = base
    return i

#heap
def head_sort(list):
    length_list = len(list)
    first = int(length_list / 2 - 1)
    for start in range(first, -1, -1):
        max_heapify(list, start, length_list - 1)
    for end in range(length_list - 1, 0, -1):
        list[end], list[0] = list[0], list[end]
        max_heapify(list, 0, end - 1)
    return list

def max_heapify(ary, start, end):
    root = start
    while True:
        child = root * 2 + 1
        if child > end:
            break
        if child + 1 <= end and ary[child] < ary[child + 1]:
            child = child + 1
        if ary[root] < ary[child]:
            ary[root], ary[child] = ary[child], ary[root]
            root = child
        else:
            break

#countSort
def count_sort(list):
    max=min=0
    for i in list:
        if i < min:
            min = i
        if i > max:
            max = i
    count = [0] * (max - min +1)
    for j in range(max-min+1):
        count[j]=0
    for index in list:
        count[index-min]+=1
    index=0
    for a in range(max-min+1):
        for c in range(count[a]):
            list[index]=a+min
            index+=1
    return list

if __name__=="__main__":
    a=[]
    for i in range(200):
        a.append(randint(0,500))
    print bubble_sort(a)



