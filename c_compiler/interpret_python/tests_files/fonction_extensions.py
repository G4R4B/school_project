def simple_generator():
    yield 1
    yield 2
    yield 3
print([[]])
gen = simple_generator()
for value in gen:
    print(value)


def infinite_sequence():
    n = 0
    while True:
        yield n
        n = n + 1

for i in infinite_sequence():
    print("gen infinite", i)
    print(i)
    if i > 10:
        break

print("done")
def count_up_to(max_value):
    count = 0
    while count < max_value:
        yield count
        count = count + 1

for value in count_up_to(5):
    print(value)

print("done")
def func1():
    print("func1")

def func2():
    print("func2")

def func3():
    print("func3")

def tuple_with_generator():
    return (1, 2, infinite_sequence())

tup = tuple_with_generator()
print((1,2,3))
print(tup[0])
print(tup[1])

def square(n):
    return n * 2

def conditional_yield(lst):
    for i in lst:
        if i % 2 == 0:
            yield i

even_gen = conditional_yield([1, 2, 3, 4, 5])
for value in even_gen:
    print(value)


def tuple_yield_gen():
    for i in range(3):
        yield (i, i + 1)

for t in tuple_yield_gen():
    print(t)


def generate_list():
    n = 0
    while True:
        yield n
        n = n + 2
        if n > 1000:
            break

infinite_list = [i for i in generate_list()]
print(infinite_list)
