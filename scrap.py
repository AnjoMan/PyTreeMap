import numpy as np

class Tree:
    
    def __init__(self, level = 0, value=np.random.rand()):
        self.level = level
        self.value = value
        self.children = [];
    
    def addChild(self, child=[],level=None):
        
        if level==None:
            level = self.level+1
        
        self.children += [Tree(level=level)]
        return self.children[-1]
    
    def __str__(self):
        string = "  "*self.level+"Tree, level: "+ str(self.level)+ "; " + str(len(self.children)) + " children, note: " + (self.note if hasattr(self, 'note') else "n/a")
        
        for child in self.children:
            string += "\n" +  child.__str__()
        
        return string


def buildTree(parent=None):
    
    
    if parent == None:
        parent = Tree(level=0)
     
    level = parent.level+1
    
    if level > 5:
        return []
    else:
        
        child = parent.addChild(Tree(level = level))
        buildTree(parent = child)
        return parent
    
    
    
    
    


myTree = buildTree()
print myTree