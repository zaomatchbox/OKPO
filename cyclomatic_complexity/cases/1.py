import os
import sys


def a(x):
    print(x)


def b(x):
    res = 1 if x > 0 else 0
    return res

d = 1
while 0 < d < 10 :
    if d % 2 == 0:
        print(a(d))
    elif d % 3 == 0:
        print(3)
    elif d % 5 == 0:
        print(5)
    else:
        print('124')
        print('123')


if __name__ == "__main__":
    a(1)
    c = b(10)
    print(c)

