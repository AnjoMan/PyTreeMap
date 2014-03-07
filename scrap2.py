

a = [1,2,3,4,5]


def remove(a):
    a = [el for  ind,el in enumerate(a) if ind not in [1,3]]
    return a
    
    
b = remove(a)


print(a)
print(b)