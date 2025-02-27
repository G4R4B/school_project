arr = [1, 2, 3]
arr[0] = 10
arr[1] = 20
arr[2] = 30
print(arr)

nested_arr = [[1, 2], [3, 4], [5, 6]]
print(nested_arr[0][1]) 
print(nested_arr[1][0])
print(nested_arr[2][1]) 

nested_arr[0][1] = 100
nested_arr[1][0] = 300
nested_arr[2][1] = 600
print(nested_arr)

mixed_arr = [1, "string", [3, 4], True]
print(mixed_arr[0])
print(mixed_arr[1]) 
print(mixed_arr[2]) 
print(mixed_arr[3]) 

mixed_arr[0] = "new_value"
mixed_arr[2][1] = 100
print(mixed_arr)

outer_array = [[1, 2, 3], [4, 5, 6]]
outer_array[0][2] = 300
outer_array[1][0] = 400
print(outer_array)

array = [1, 2, 3, 4, 5]
print(len(array))

large_array = list(range(100))
print(large_array[50])
print(large_array[99])

large_array[99] = 999
print(large_array[99])

nested_large = [[[i for i in range(10)] for _ in range(10)] for __ in range(10)]
print(nested_large[9][9][9])
print(nested_large[0][0][0])
nested_large[9][9][9] = 9999
nested_large[0][0][0] = 1111
print(nested_large[9][9][9])
print(nested_large[0][0][0])
print(nested_large)

a = [1, 2, 3]
b = a
b[0] = 100
print(a)
print(b)

bool_arr = [True, False, True]
print(bool_arr[0])
print(bool_arr[1])

bool_arr[1] = True
print(bool_arr)
