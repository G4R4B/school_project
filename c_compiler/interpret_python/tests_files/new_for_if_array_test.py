
arr = [1, 2, 3]
for i in arr:
    print(i)


arr = [1, 2, 3]
for i in range(len(arr)):
    arr[i] = arr[i] + 1
print(arr)


arr = [1, 2, 3, 4, 5]
for i in arr:
    if i % 2 == 0:
        print("Even")
    else:
        print("Odd")


for i in range(5):
    print(i)


arr = [0, 5, 10, 15, 20]
for i in arr:
    if i > 10:
        print("Greater than 10")
    else:
        print("10 or less")


matrix = [[1, 2], [3, 4], [5, 6]]
for row in matrix:
    for element in row:
        print(element)


arr = ["apple", "banana", "cherry"]
for fruit in arr:
    if fruit == "banana":
        print("Found banana")
    else:
        print(fruit)


arr = [10, 20, 30]
if arr[1] == 20:
    print("Second element is 20")
else:
    print("Second element is not 20")


arr = [1, 2, 3, 4, 5]
for i in arr:
    if i == 3:
        break
    print(i)

arr = [1, 2, 3, 4, 5]
for i in arr:
    if i == 3:
        continue
    print(i)


s = "hello"
for char in s:
    print(char)


arr = [0, 1, 2, 3]
for i in range(len(arr)):
    if arr[i] % 2 == 0:
        arr[i] = arr[i] * 2
print(arr)


arr = [10, 5, 0, -5, -10]
for i in range(len(arr)):
    if arr[i] < 0:
        arr[i] = 0
print(arr)


arr = [1, 2, 3]
for i in range(len(arr)):
    if arr[i] == 2:
        arr[i] = 20
print(arr)


matrix = [[10, 20], [30, 40], [50, 60]]
for row in matrix:
    for val in row:
        if val > 30:
            print("Greater than 30:", val)
        else:
            print("30 or less:", val)


arr = [5, 10, 15]
for i in range(len(arr)):
    if i == 1:
        print("Index 1 value:", arr[i])


arr = [1, 2, 3]
for i in arr:
    for j in arr:
        print(i + j)

while True:
    if True:
        if True:
            break
    else:
        continue
