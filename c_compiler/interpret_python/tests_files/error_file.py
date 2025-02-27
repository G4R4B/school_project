a = [1,2,3]
if None:
    a
def f(a):
    if False:
        a
    if True:
        a
    if a:
        a
    return a

def g(b):
    b[0] = 2
g(a)
def h(c, d, e):
    c[0] = 3
    d[0] = 3
    e[0] = 3
h(a, a, a)
print(a)
print([[[[[[[[[]]]]]]]]])
if (a[2] == 3):
    if (a[1] == 2):
        if (a[0] == 1):
            print("a is [1,2,3]")
        else:
            print("b")
    else:
        print("b")
else:
    print("b")
