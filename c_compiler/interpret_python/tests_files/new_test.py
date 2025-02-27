def f(x):
    return x+3

def k(x):
    for i in range(5):
        print(i)
        if i == 3:
            return i
        
def myrange(n):
    if n > 0:
        return myrange(n-1) + [n-1] + myrange(n-1)
    else:   
        return []
    
print(myrange(5))