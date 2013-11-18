

class A(object):
    
    def __init__(self, val, lab):
        self.val = val
        self.lab = lab
    def __repr__(self):
        return self.lab + (' %04d' % self.val)
    def __hash__(self):
        return hash( repr(self))
    
    def __cmp__(self, other):
        if self.lab< other.lab: return -1
        
        elif self.lab > other.lab: return 1
        
        else:
            return self.val - other.val
        
        

labels = ['Vic', 'Vic', 'Forth', 'Rog']

mList = [A(i,label) for i, label in enumerate(labels)]


print mList
print sorted(mList)


    