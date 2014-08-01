from VisBuilder import *
import ast

def main():
    
    
    file = 'cpfResults_case118_2level'
    
    mCPFfile = CPFfile(file)
#     mElements = mCPFfile.Branches + mCPFfile.Buses
    mElements = mCPFfile.getElementList()
    
    
    mel = mElements[0]
    
    import json
    with open('case118_geometry.json','w') as f:
        ds = [el.toDict() for el in mElements]
        json.dump(ds, f, indent=4)
#         for el in mElements:
#             json.dump(el.toDict(),f, indent=4)
    
    
    
    
    
    with open('case118_geometry.json', 'r') as f:
        x = json.load(f)
    
    
#     a = ast.literal_eval(x[0])
    
    
    print('wait');
        
if __name__ == "__main__":
    main()