def test_if_true():
    if True:
        print("True branch")

def test_if_false():
    if False:
        print("False branch")
        
test_if_true()
test_if_false()

def test_for_simple():
    for i in [1, 2, 3]:
        print(i)

test_for_simple()

def test_for_break():
    for i in [1, 2, 3]:
        if i == 2:
            break
        print(i)

test_for_break()

def test_for_continue():
    for i in [1, 2, 3]:
        if i == 2:
            continue
        print(i)

test_for_continue()

def test_for_if():
    for i in [1, 2, 3, 4]:
        if i % 2 == 0:
            print(i, "is even")

test_for_if()

def test_for_if_else():
    for i in [1, 2, 3, 4]:
        if i % 2 == 0:
            print(i, "is even")
        else:
            print(i, "is odd")

test_for_if_else()

def test_nested_for():
    for i in [1, 2]:
        for j in [3, 4]:
            print(i, j)

test_nested_for()


def test_for_sum(nums):
    total = 0
    for num in nums:
        total = total + num
    return total

print(test_for_sum([1, 2, 3]))


def test_if_return(val):
    if val:
        return "True"
    else:
        return "False"

def test_if_else(val):
    if val > 0:
        return "Positive"
    else:
        return "Non-positive"

print(test_if_else(5))
print(test_if_else(-1))


print(test_if_return(0))
print(test_if_return(1))
print(test_if_return([]))
print(test_if_return([1]))
