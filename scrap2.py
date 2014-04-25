



class Apple(object):
    
    def __init__(self):
        
        self._mList = []
    
    
    @property
    def mList(self):
        return self._mList
    




mApple = Apple()



mApple.mList.append(1)



print(mApple.mList)

mApple.mList.append(25)


print(mApple.mList)