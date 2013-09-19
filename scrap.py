class Circle(object):
    
    def __init__(self, id):
        self.id = id
    
    def __repr__(self):
        return 'Circle, id: %d' % self.id




def createObj(object, id):
    return object(id)





newCircle = createObj(Circle, 2)

print newCircle