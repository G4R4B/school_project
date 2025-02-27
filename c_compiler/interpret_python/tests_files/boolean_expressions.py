
print(True)
print(False)


print(not True)
print(not False)


print(True and True)
print(True and False)
print(False and True)
print(False and False)


print(True or True)
print(True or False)
print(False or True)
print(False or False)


print(True == True)
print(True == False)
print(False == False)
print(True != False)
print(False != False)


print(True > False)
print(False > True)
print(True >= True)
print(False <= True)
print(True < False)


print((True and False) or True)
print((True or False) and (not False))
print((False or False) and True)


print(0 and True)
print(1 and True)
print(1 or False)
print(0 or True)
print(0 or False)


print(True == 1)
print(False == 0)
print(True != 0)
print(False != 1)


print(True + 1)
print(False + 1)
print(True * 10)
print(False * 10)


bool_list = [True, False, True]
print(bool_list[0])
print(bool_list[1])
print(bool_list[-1])


bool_list[1] = not bool_list[1]
print(bool_list)


print(True == "True")
print(False == "")
print(True != "False")


print("string" and True)
print("" or False)
print([] or True)
print([1, 2] and False)


print(None or True)
print(None and True)
print(True and None)
print(False or None)


x = True
y = False
z = True
print((x and y) or (not z))
print((x or y) and (z or not x))


print((1 < 2) == True)
print((0 > -1) == False)
print(((0 < 1) > False) == True)


print(not not True)
print(not not False)
print(not not not True)


def bool_func(a, b):
    return a and b

print("here")
print(bool_func(True, False))
print(bool_func(True, True))


print((True + 2) * 3)
print((False + 5) // 2)