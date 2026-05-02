import time
def bubbleSort(daList):
    daList.time_start = time.perf_counter()
    n = len(daList.data)

    while n > 1:
        swapped = False
        last_swap = 0
        a = daList.read(0)

        for j in range(n - 1):
            b = daList.read(j + 1)

            if a > b:
                daList.write(j, b)
                daList.write(j + 1, a)
                swapped = True
                last_swap = j + 1
            else:
                a = b

        if not swapped:
            break

        n = last_swap

def shaker(daList):
    left = 0
    right = len(daList.data) - 1
    while left < right:
        swapped = False
        last_swap = left
        a = daList.read(left)
        for j in range(left, right):
            b = daList.read(j + 1)
            if a > b:
                daList.write(j, b)
                daList.write(j + 1, a)
                swapped = True
                last_swap = j
            else:
                a = b
        if not swapped:
            break
        right = last_swap
        swapped = False
        last_swap = right
        a = daList.read(right)
        for j in range(right, left, -1):
            b = daList.read(j - 1)
            if b > a:
                daList.write(j, b)
                daList.write(j - 1, a)
                swapped = True
                last_swap = j
            else:
                a = b
        if not swapped:
            break
        left = last_swap

def selectionSort(daList):
    n = len(daList.data)
    for i in range(n-1):
        min_index = i
        min_value = daList.read(i)
        for j in range(i+1,n):
            value = daList.read(j)
            if value<min_value:
                min_index = j
                min_value = value
        if min_index != i:
            old_value = daList.read(i)
            daList.write(i,min_value)
            daList.write(min_index,old_value)

def insertionSort(daList):
    n=len(daList.data)
    for i in range(1,n):
        key=daList.read(i)
        j=i-1
        while j>=0:
            current=daList.read(j)
            if current<=key:
                break
            daList.write(j+1,current)
            j-=1
        if j+1!=i:
            daList.write(j+1,key)
def gnomeSort(daList):
    n=len(daList.data)
    i=1
    while i<n:
        if i==0:
            i=1
        a=daList.read(i-1)
        b=daList.read(i)
        if a<=b:
            i+=1
        else:
            daList.write(i-1,b)
            daList.write(i,a)
            i-=1
def oddEvenSort(daList):
    n=len(daList.data)
    sorted=False
    while not sorted:
        sorted=True
        for i in range(1,n-1,2):
            a=daList.read(i)
            b=daList.read(i+1)
            if a>b:
                daList.write(i,b)
                daList.write(i+1,a)
                sorted=False
        for i in range(0,n-1,2):
            a=daList.read(i)
            b=daList.read(i+1)
            if a>b:
                daList.write(i,b)
                daList.write(i+1,a)
                sorted=False
def combSort(daList):
    n=len(daList.data)
    gap=n
    shrink=1.3
    sorted=False
    while not sorted:
        gap=int(gap/shrink)
        if gap<=1:
            gap=1
            sorted=True
        for i in range(n-gap):
            a=daList.read(i)
            b=daList.read(i+gap)
            if a>b:
                daList.write(i,b)
                daList.write(i+gap,a)
                sorted=False

