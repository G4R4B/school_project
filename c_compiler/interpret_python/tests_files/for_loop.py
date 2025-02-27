
for i in range(5):
    print(i)

for i in range(0):
    print(i)
for i in range(100, 10, -10):
    print(i)

for i in range(10, 12):
    print(2*i)

for x in [1, 2, 3, 4]:
    print(x)


for i in range(3):
    for j in range(2):
        print(i, j)


for char in "hello":
    print(char)


for x in []:
    print(x)
    

for sublist in [[1, 2], [3, 4], [5, 6]]:
    for item in sublist:
        print(item)


for i in range(0, 10, 2):
    print(i)


for i in range(5, 0, -1):
    print(i)


numbers = [i for i in range(4)]
for n in numbers:
    print(n)


for i in range(3):
    print(i + 2)


for item in [1, "string", True, None]:
    print(item)


for i in range(3):
    print(i)

for i in reversed(range(4)):
    print(i)

my_list = [1, 2, 3, 4]
idx = 1
for i in my_list:
    my_list[idx] = i * 10
    print(my_list, i)

for i in range(10):
    if i % 3 == 0:
        print(i)

a = [1, 2, 3]
for a in a:
    print(a)
print(a)