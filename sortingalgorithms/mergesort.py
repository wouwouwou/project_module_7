"""
Includes functions which include mergesort algorithms for lists of different types.
 msintlist:		mergesort algorithm for a list of integers
"""


def msintlist(a):
    if len(a) > 1:
        mid = len(a) // 2
        lefthalf = a[:mid]
        righthalf = a[mid:]

        msintlist(lefthalf)
        msintlist(righthalf)

        i = 0
        j = 0
        k = 0
        while i < len(lefthalf) and j < len(righthalf):
            if lefthalf[i] < righthalf[j]:
                a[k] = lefthalf[i]
                i += 1
            else:
                a[k] = righthalf[j]
                j += 1
            k += 1

        while i < len(lefthalf):
            a[k] = lefthalf[i]
            i += 1
            k += 1

        while j < len(righthalf):
            a[k] = righthalf[j]
            j += 1
            k += 1