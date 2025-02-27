t = (1, 2, 3)
print(t)
print(t[0])
print(len(t))

t = (4, 5, 6) #comment
for i in t:
    print(i)


t = (1, "string", True)
print(t[0])
print(t[1])
print(t[2])


t = (1, (2, 3), 4)
print(t[1])
print(t[1][1])


def return_tuple():
    return (10, 20, 30)

result = return_tuple()
print(result)


t1 = (1, 2, 3)
t2 = (1, 2, 4)
t3 = (1, 2, 3)
print(t1 < t2)
print(t1 == t3)