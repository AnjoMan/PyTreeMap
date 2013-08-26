import numpy as np
from matplotlib import pyplot as plt
from collections import defaultdict

class Element():
    geo = defaultdict(None)
    
    def __init__(self, id=0, value=None):
        self.id=id
        self.value = value if value != None else np.random.rand()
    
    
    def __repr__(self):
        return self.__class__.__name__ + " %04d" % self.id
    
    def __eq__(self, other):
        return True if self.__class__.__name__ == other.__class__.__name__ and self.id == other.id else False
    
    def __hash__(self):
        #has the string representation of the element, eg 'bus 01'
        return hash(str(self))
    
    def getGeo(self):
        return Element.geo[self.__class__][self.id]
    
    def secondary(self):
        geo = self.getGeo()
        return geo
    
    @staticmethod
    def setgeo(geo):
        Element.geo = geo

class Branch(Element):
    def secondary(self):
        geo = self.getGeo()
        return Line(geo).getPosition()
        
        

class Bus(Element): pass

class Gen(Element): pass

class Transformer(Element): pass
    
class Fault:
    
    def __init__(self,listing, reduction = None):
        #ideally processing of input data to produce listings should be done outside of this, since it is input-data specific
        
        label, branch, bus, gen = listing; 
#         print branch
        
#         for el in branch: print el
#         listing = listing[0][0]
        self.label = label
        self.reduction = reduction
        
#         def getList(myList):
#             zeroDim = [element for element in myList.shape if element != 0L]
#             return [element for element in listing.branch[0]] if len(zeroDim) > 1 else []
        
        self.elements = []
        self.elements += [Branch(id=item) for item in branch]
        self.elements += [Bus(id=item) for item in bus]
        self.elements += [Gen(id=item) for item in gen]
        
        
    
    def __repr__(self):
        return 'Fault, ({})'.format(repr(self.elements))
    def __str__(self):
        def typeIds(mType): return [el.id for el in self.elements if el.__class__.__name__ == mType]
        branch, bus, gen = [typeIds(mType) for mType in [Element.Branch, Element.Bus, Element.Gen]]
        string = '\t\t'.join([self.label, 'CPF: %.3f' % self.reduction, 'elements:', str(branch), str(bus), str(gen)])
        string = '\n%s' % string
        
        return string
    
    def value(self):
        return self.reduction
    
    def getElements(self):
        return self.elements
    
    def strip(self, stripElement):
        self.elements = [el for el in self.elements if el != stripElement]
    
    def subFault(self, element):
        from copy import copy
        newFault = copy(self)
        newFault.strip(element)
        return newFault

class Line:
    def __init__(self, myNodes):
        self.nodesX = myNodes[0]
        self.nodesY = myNodes[1]
    
    def draw(self,axes, color="#0000FF"):
        for index in range(0, len(self.nodesX)-1):
            axes.plot( self.nodesX[index:index+2], self.nodesY[index:index+2], c=color)
    
    def getLength(self):
        sum = 0;
        for index in range(0,len(self.nodesX)-1):
            sum += np.sqrt(  (self.nodesX[index+1]-self.nodesX[index])**2 + (self.nodesY[index+1]-self.nodesY[index])**2)
        return sum
    
    def getMidpoint(self):
        
        if not hasattr(self, 'midPoint'):
            #get distance between each point
            deltaDistances = lambda array: [b-a for a,b in zip(array[0:-1],array[1:])]
            
            dxs,dys = deltaDistances(self.nodesX), deltaDistances(self.nodesY)
            
            
            distances = [0] + [ np.sqrt(dx**2 + dy**2) for dx,dy in zip(dxs, dys)]  
            
            length = np.sum(distances);
            
            cumDistances = np.cumsum(distances)
            
            #max index of distances s.t. cumsum <= half total length
            ltHalves = [index for index,value in enumerate(cumDistances) if value <= length/2]
            lt_half = np.max(ltHalves)
            
            percentAlong = (length/2 - cumDistances[lt_half])/ distances[lt_half+1]
            
            lineBisect = lambda array: array[0] + percentAlong * (array[1]-array[0])
            xM,yM = lineBisect(self.nodesX[lt_half:lt_half+2]), lineBisect(self.nodesY[lt_half:lt_half+2])
            
            self.midPoint = xM,yM
        
        return self.midPoint
    
    def getPosition(self):
        return self.getMidpoint()
        

def main():
    
    X = [1,2,2+1/np.sqrt(2)]
    Y = [4,5,5+1/np.sqrt(2)]
    
    a = Line(np.array([ X,Y]))
    
    x,y = a.getPosition()
    
    
    plt.scatter(X,Y);
    
    plt.scatter(x,y,c="#00FF00")
    plt.show()


    
if __name__ == "__main__":
    main()