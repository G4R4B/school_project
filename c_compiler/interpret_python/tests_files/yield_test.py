
def h():
    n = 0
    while True:
        yield n
        n = n + 1
        

for i in h():
    if i > 10:
        break
    print(i)
