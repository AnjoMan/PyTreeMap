from collections import defaultdict


def defaultIZE(dictionary,default_factory=list):
    newDict = defaultdict(default_factory)
    for k,v in dictionary.items():
        newDict[k]=v
    
    return newDict

a = {id: value for id,value in zip( [1,2,3,4], ['a','b','c','c'])}

b = defaultIZE(a)


c = [1,2,5]


print [b[el] for el in c]



