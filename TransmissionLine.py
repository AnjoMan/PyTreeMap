import numpy as np
from matplotlib import pyplot as plt

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