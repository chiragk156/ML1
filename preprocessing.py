import random

# Feature Selection

def merge(arr, arr1, l, m, r):
    n1 = m - l + 1
    n2 = r- m
 
    # create temp arrays
    L = [0] * (n1)
    R = [0] * (n2)
    L1 = [0] * (n1)
    R1 = [0] * (n2)
 
    # Copy data to temp arrays L[] and R[]
    for i in range(0 , n1):
        L[i] = arr[l + i]
        L1[i] = arr1[l + i]
 
    for j in range(0 , n2):
        R[j] = arr[m + 1 + j]
        R1[j] = arr1[m + 1 + j]
 
    # Merge the temp arrays back into arr[l..r]
    i = 0     # Initial index of first subarray
    j = 0     # Initial index of second subarray
    k = l     # Initial index of merged subarray
 
    while i < n1 and j < n2 :
        if L[i] <= R[j]:
            arr[k] = L[i]
            arr1[k] = L1[i]
            i += 1
        else:
            arr[k] = R[j]
            arr1[k] = R1[j]
            j += 1
        k += 1
 
    # Copy the remaining elements of L[], if there
    # are any
    while i < n1:
        arr[k] = L[i]
        arr1[k] = L1[i]
        i += 1
        k += 1
 
    # Copy the remaining elements of R[], if there
    # are any
    while j < n2:
        arr[k] = R[j]
        arr1[k] = R1[j]
        j += 1
        k += 1
 
# l is for left index and r is right index of the
# sub-array of arr to be sorted
def mergeSort(arr,arr1,l,r):
    if l < r:
 
        # Same as (l+r)/2, but avoids overflow for
        # large l and h
        m = (l+(r-1))/2
 
        # Sort first and second halves
        mergeSort(arr,arr1, l, m)
        mergeSort(arr,arr1, m+1, r)
        merge(arr,arr1, l, m, r)


# Reading from file
file = open('../data/imdbEr.txt','r')
values = file.read().split('\n')
file.close()
if '' in values:
    values.remove('')

n=len(values)

for i in range(0,n):
	values[i]=float(values[i])

indices = range(0,n)

# Sorting indices array based on values
mergeSort(values,indices,0,n-1)


# Top and least
tl = 2500
least2500 = indices[:tl]
top2500 = indices[n-tl:]

file = open('selected-features-indices.txt','w')
for i in range(0,tl-1):
	file.write(str(least2500[i])+'\n')
	file.write(str(top2500[i])+'\n')
file.write(str(least2500[tl-1])+'\n')
file.write(str(top2500[tl-1]))	
file.close()




# Training data selection
file = open('../data/train/labeledBow.feat','r')
file1 = open('trainingdata.txt','w')
data = file.read().split('\n')
if '' in data:
    data.remove('')
file.close()
pos=500
neg=500
r=random.sample(range(0, len(data)), len(data))
temp=0
while pos!=0 or neg!=0:
    if int(data[r[temp]].split(' ')[0])>=7:
        if pos>0:
            file1.write(data[r[temp]]+'\n')
            pos-=1
    elif int(data[r[temp]].split(' ')[0])<=4:
        if neg>0:
            file1.write(data[r[temp]]+'\n')
            neg-=1
    temp+=1
file1.close()


# Testing data selection
file = open('../data/test/labeledBow.feat','r')
file1 = open('testingdata.txt','w')
data = file.read().split('\n')
if '' in data:
    data.remove('')
file.close()
pos=500
neg=500
r=random.sample(range(0, len(data)), len(data))
temp=0
while pos!=0 or neg!=0:
    if int(data[r[temp]].split(' ')[0])>=7:
        if pos>0:
            file1.write(data[r[temp]]+'\n')
            pos-=1
    elif int(data[r[temp]].split(' ')[0])<=4:
        if neg>0:
            file1.write(data[r[temp]]+'\n')
            neg-=1
    temp+=1
file1.close()