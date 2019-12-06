import numpy

a = numpy.asarray([1, 2, 3, 4])

def s(a):
    a[1] = 1111

s(a)
print(a)