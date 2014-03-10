

a = [1,2,3,4,5]


move = 2;




b = [6,7]
print(a,b)

b = a[len(a)-move:] + b
a = a[0:len(a)-move]

print(a,b)