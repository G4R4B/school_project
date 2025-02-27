arr = [1, 2, 3, 4, 5]
if len(arr) > 3:
    print("List is longer than 3 elements")
else:
    print("List has 3 or fewer elements")
arr = [10, 20, 30] 
if arr[0] < 10:
    print("First element is less than 10")
else:
    print("First element is greater than 10")


arr = []
if not arr:
    print("The list is empty")
else:
    print("The list is not empty")


arr = [5, 8, 2, 7]
for num in arr:
    if num > 5:
        if num % 2 == 0:
            print(num, " is greater than 5 and is even")
        else:
            print(num, " is greater than 5 and is odd")
    else:
        print(num, " is less than or equal to 5")


arr_of_arrs = [[1, 2, 3], [4, 5], [6, 7, 8, 9]]
for sublist in arr_of_arrs:
    for item in sublist:
        print(item)


arr = ["apple", "banana", "cherry"]
for i in range(len(arr)):
    print("Index", i, ":", arr[i])


arr = [1, 2, 3, 4]
for i in range(len(arr)):
    arr[i] = arr[i] * 2
print(arr)


arr = [10, 20, 30, 40, 50]
for num in arr:
    if num > 25:
        print("Breaking at", num)
        break
    print("Checking", num)


arr = [15, 22, 30, 18, 25]
for num in arr:
    if num % 2 != 0:
        continue
    print(num, "is even")

arr = [1, 2, 3, 4, 5]
squared = [x * x for x in arr]
print(squared)


arr = [10, 20, 30, 40, 50]
for num in reversed(arr):
    print(num)


arr1 = [1, 2, 3]
arr2 = [3, 2, 1]
if arr1 == arr2:
    print("Arrays are equal")


arr = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
found = False
for sublist in arr:
    for num in sublist:
        if num == 5:
            print("Found 5, exiting...")
            found = True
            break
    if found:
        break


arr = [1, 2, 3, 4]
if arr[0] == 1 and arr[-1] == 4:
    print("First element is 1 and last element is 4")


arr = [10, 20, 30, 40]
if arr[-1] == 40:
    print("The last element is 40")


arr = [1, 2, 3, 4, 5]
for i in range(5):
    arr[i] = arr[i] * 10
print(arr)


arr1 = [1, 2, 3]
arr2 = [4, 5, 6]
for i in range(len(arr1)):
    arr1[i] = arr1[i] + 1
    arr2[i] = arr2[i] * 2
print(arr1)
print(arr2)


arr = [10, 20, 30]
total = 0
for num in arr:
    total = total + num
print("Total:", total)