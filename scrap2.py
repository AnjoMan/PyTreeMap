from numpy import *
import random
import matplotlib.pyplot as plt



numbers =[random.randint(-3, 10) for i in range(0,40)]

print(numbers)



plt.scatter(range(0,len(numbers)),numbers)

def normalize(x):
    x = array(x)
    x = x - min(x)
    x = x / max(x)
    return x

newNumbers = normalize(numbers)

plt.scatter(range(0,len(numbers)), newNumbers, color = 'red')


plt.show()