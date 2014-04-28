



class Apple(object):
    
    def __init__(self):
        
        self._mList = []
        self.mList = []
    
    
    @property
    def mList(self):
        return self._mList
    
    @mList.setter
    def mList(self,x):
        self._mList = x
    




mApple = Apple()



mApple.mList.append(1)



print(mApple.mList)

mApple.mList.append(25)


print(mApple.mList)

mApple.mList = [1,2,3] or []

print(mApple.mList)