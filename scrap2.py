class Fault(object):
    
    def __init__(self, value):
        self.value = value
        self._subValue = None
    
    
    @property
    def subValue(self):
        return self._subValue or self.value * 10


mFault = Fault(20)


print(mFault.value)
print(mFault.subValue)