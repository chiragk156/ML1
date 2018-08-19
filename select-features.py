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
file = open('imdbEr.txt','r')
values = file.read().split('\n')
file.close()
values.remove('')

n=len(values)

for i in range(0,n):
	values[i]=float(values[i])

indices = range(0,n)

# Sorting indices array based on values
mergeSort(values,indices,0,n-1)

least2500 = indices[:2500]
top2500 = indices[n-2500:]

file = open('selected-features-indices.txt','w')
for i in range(0,2499):
	file.write(str(least2500[i])+'\n')
	file.write(str(top2500[i])+'\n')
file.write(str(least2500[2499])+'\n')
file.write(str(top2500[2499]))	
file.close()