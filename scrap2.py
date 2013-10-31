from numpy import *




mArray =[ [ [1,-1], [2,-2], [3,-3]], [ [1,-1], [2,-2], [3,-3]]]


def negateY(element):
    element = transpose(array(element))
    element = transpose([list(element[0]), list(element[1]*-1)])
    element = [list(point) for point in element]
    return element
    
 


nArray = [negateY(el) for el in mArray]

