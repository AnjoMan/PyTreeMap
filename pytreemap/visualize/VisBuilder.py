"""
    written by Anton Lodder 2012-2014
    all rights reserved.
    
    This software is the property of the author and may not be copied,
    sold or redistributed without expressed consent of the author.
"""

if __name__ == '__main__':
    import sys, os, inspect
    try:
        import pytreemap
    except:
        #walk up to 'pytreemap' and add to path.
        realpath = os.path.realpath(os.path.dirname(inspect.getfile(inspect.currentframe())))
        (realpath, filename) = os.path.split(realpath)
        while filename != 'pytreemap':
            (realpath, filename) = os.path.split(realpath)
        sys.path.append(realpath)
        import pytreemap
    

from numpy import *
from collections import defaultdict

from pytreemap.system.PowerNetwork import Bus, Branch, Gen, Transformer

def main():
    
    from pytreemap.visualize.TreemapGraphics import TreemapFault
    
    file = 'cpfResults_4branches'
    
    file = os.path.join(pytreemap.__path__[0], 'sample_results', file)
    
    
    mCase = (os.path.join(pytreemap.__path__[0], 'sample_results', 'cpfResults_small.json'), os.path.join(pytreemap.__path__[0], 'system','case30_geometry.json'))
    
    
    print('Creating JSON File')
    mCPFresults_JSON = JSON_systemFile(*mCase)
    
    
    print('\nCreating MATLAB File')
    mCPFresults_MATLAB = MATLAB_systemFile(file)
    

#     elements = mCPFresults.getElements()
    
    print('\nGetting Faults from JSON File')
    (faults_JSON, faultTree_JSON) = getFaults(TreemapFault, mCPFresults_JSON)
    print('\nGetting Faults from MATLAB File')
    (faults_MATLAB, faultTree_MATLAB) = getFaults(TreemapFault, mCPFresults_MATLAB)
    
    
    print('runs')
    
    



class doneLog(object):
    def __init__(self, message, reportFunc=None):
        self.message = message
        self.reportFunc = reportFunc
    def __call__(self, f):
        from functools import wraps
        @wraps(f)
        def wrapped(*args, **kwargs):
            out = f(*args, **kwargs)
            print("\t|| {}{}".format(self.message, " - {}".format(self.reportFunc(out)) if self.reportFunc else ""))
            return out
        
        return wrapped

def log(string):
    print("\t" + '|| ' + string)



def getFaults(FaultType, cpfFile, filter=0):
    #get faults
    
    @doneLog("faultTree created", lambda x: "{} levels".format(len(x)))
    def buildFaultTree(faults):
        """ From a flat list of faults, build a dictionary that divides the faults by n-i contingency level. """
    
        faultTree = defaultdict(list)
        #sort faults by number of element in each
        for fault in faults:
            faultTree[len(fault.getElements())] += [fault]
        
        if 0 in faultTree:
            del faultTree[0]
        
        return faultTree
    
    @doneLog("Connections Built")
    def buildConnections(faults, faultTree):
        """ Go over each fault give it a list of sub-faults to track. """
        #get fault position masks by element    
        maskLength = len(faults)
        faultByElement = defaultdict(int)
        for index, fault in enumerate(faults):
            for element in fault.elements:
                faultByElement[element] += 1<<index
        
    
        def int2bool(i,n): return fromiter( ((False,True)[i>>j & 1] for j in range(0,n) ), bool)
        def trueIndices(i,n): return (j for j in range(0,n) if i>>j & 1)
        
        log('fault indexes listed per-element')
        
        
        keys = sorted(faultTree.keys())
        keys.reverse()
        
    #     #identify connections
        keys = sorted(faultTree.keys())
        
        faultsArray=array(faults)
        for level in keys[0:-1]:
            for fault in faultTree[level]:
                masks = (faultByElement[element] for element in fault.elements)
                mask = masks.__next__()
                for el in masks:
                    mask = mask & el
                
                subFaults = (faults[i] for i in trueIndices(mask, maskLength) if len(faults[i].elements) == 1+level)
                for subFault in subFaults:
                    fault.addConnection(subFault)
    
    @doneLog('Context Limits Set')
    def setContextLimits(FaultType, faults):
        """ Set limits for context getter, allowing fault to be evaluated in context of its level. Used by Tree. """
        values = [fault.value for fault in faults]
        FaultType.setGlobalContext(min(values),  max(values))
        for level, levelFaults in faultTree.items():
            values = [fault.value for fault in levelFaults]
            FaultType.setLevelContext(level, min(values), max(values))
            
            values = [fault.subValue for fault in levelFaults]
            FaultType.setCumulativeContext(level, min(values), max(values))
    
    
    @doneLog('Normalized Secondary Values')
    def normalizeSecondaries(faults):
        """ Normalize secondary values so faults can be displayed on the same scale. """
        
        #normalize secondaries
        def normalize(x):
            #identify indices of  None
            nonIndexes = [i for i, el in enumerate(x) if el is None]
            
            if len(nonIndexes) < len(x):
                #replace None with 0 so we can do math on it
                x = [el if el else 0 for el in x]
                
                
                #perform mask
                x = array(x)
                x = x - min(x)
                x = x / max(x)
            
                #put Nones back where indicated by nonIndexes
                x = [el if i not in nonIndexes else None for i,el in enumerate(x) ]
                
            return x
            
        #initialize and get secondary values for all faults.
        secondaryValues = [fault.secondary for fault in faults]
        secondaryValues = normalize(secondaryValues)
        for value, fault in zip(secondaryValues, faults):
            fault.secondary = value;
    
    
    
    #run the various methods
    faults = cpfFile.getFaults(FaultType, filter=filter)
    faultTree = buildFaultTree(faults)
    buildConnections(faults, faultTree)
    setContextLimits(FaultType, faults)
    normalizeSecondaries(faults)
    return faults, faultTree



class ResultsFile(object):
    
    @property
    def Branches(self):
        return list( self.getElements()[Branch].values() )
    
    @property
    def Buses(self):
        return  list( self.getElements()[Bus].values() )
    
    @property
    def Transformers(self):
        return  list( self.getElements()[Transformer].values() )
    
    @property
    def Generators(self):
        return  list( self.getElements()[Gen].values() )
        
    @property
    def baseLoad(self):
        try:
            return self._baseLoad
        except:
            self._baseLoad = self.getBaseLoad()
            return self._baseLoad
            
    def getElementList(self):
        elements = self.getElements()
        
        elList = []
        for elTypeList in sorted(elements.values(), key= lambda x: x.__class__.__name__):
            elList += list(elTypeList.values())
        
        return elList
    
    def getFaults(self, FaultType, filter=0):
        try:
            return self.faults
        except:
            self.faults = self.buildFaults(FaultType, filter)
            return self.faults
    
    def getElements(self):
        try:
            return self.elements
        except:
            self.elements = self.buildElements()
            return self.elements
    



class JSON_systemFile(ResultsFile):
    def __init__(self, res = None, sys=None):
        self.resultsFile = res
        
        if sys is None:
            try:
                #assume that system file is given in the results file.
                import json
                with open(res, 'r') as f:
                    results = json.load(f)
                
                self.systemFile = results['geometry_file']
                import os
                assert os.path.isfile(self.systemFile)
            except:
                log("No System File Given")
                self.systemFile = None
        else:
            self.systemFile = sys
            
        
        
    
    
    def getBaseLoad(self):
        """ How to get the base load from cpfResults.mat"""
        import json
        with open(file, 'r') as f:
            results = json.load(f)
        
        return results['baseLoad']
        
    @doneLog('Faults Created', len)
    def buildFaults(self, FaultType, filter):
        import json
        with open(self.resultsFile, 'r') as f:
            results = json.load(f)
        
        self._baseLoad = results['baseLoad']
        baseLoad = self._baseLoad
        
        elements = self.getElements()
#         mapKeys = {'Transformer':Transformer ,  'Bus':Bus,'Branch':Branch,'Gen':Gen}
        mapKeys = { Transformer:'Transformer',   Bus:'Bus',Branch:'Branch',Gen:'Gen'}
        
        
        def faultListings(faultDicts): #break out faults in JSON to list of Elements and load reduction
            for faultDict in faultDicts:
                faultEls = []
                for Type in mapKeys.keys():
                    faultEls += [elements[Type][id] for id in faultDict['elements'][mapKeys[Type]]]
                
                yield {'reduction': baseLoad-faultDict['load'], 'elements':faultEls}
        
        faults = [FaultType(listing) for listing in faultListings(results['faults'])  if listing['reduction']/baseLoad > filter/100]
        
        return faults
    
 
    @doneLog('Grid Elements Created')
    def buildElements(self):
        
        if self.systemFile == None:
            #what to do if no system file is given - identify the elements from the results file and create objects with no positional data
            import json
            with open(self.resultsFile, 'r') as f:
                results = json.load(f)
            
            from collections import defaultdict
            elDict = defaultdict(dict)
            for fault in results['faults']:
                for element, ids in fault['elements'].items():
                    for id in ids:
                        elDict[element][id] = True;
            
            
            
            mapKeys = { 'Transformer':Transformer, 'Bus':Bus, 'Branch':Branch, 'Gen':Gen}
            elements = defaultdict(dict)
            for elementType, ids in elDict.items():
                elements[mapKeys[elementType]] = {id: mapKeys[elementType](id) for id in ids}
            
            return elements
                
        else:
            #expect the elements to be in a json list of dicts, each dict should represent an element and should contain the info needed to produce that list.
            import json
            with open(self.systemFile, 'r') as f:
                elDicts = json.load(f)
                
            elements = dict()
            
            #build Buses
            busDicts = [mDict for mDict in elDicts if mDict['type'] == 'Bus']
            elements[Bus] = {el['id']: Bus(from_dict=el) for el in busDicts}
            
            #build Branches
            branchDicts = [mDict for mDict in elDicts if mDict['type'] == 'Branch']
            for mDict in branchDicts: #convert bus listings into actual Buses.
                mDict['buses'] = [elements[Bus][i] for i in mDict['buses']]
            elements[Branch] = {el['id']: Branch(from_dict=el) for el in branchDicts}
            
            #Build Generators
            genDicts = [mDict for mDict in elDicts if mDict['type'] == 'Gen']
            for mDict in genDicts:
                mDict['bus'] = elements[Bus][mDict['bus']]
            elements[Gen] = {el['id']: Gen(from_dict=el) for el in genDicts}
            
            
            transDicts = [mDict for mDict in elDicts if mDict['type'] == 'Transformer']
            for mDict in transDicts:
                mDict['connected'] = [elements[Bus][i] for i in mDict['connected']['Bus']] + [elements[Branch][i] for i in mDict['connected']['Branch']]
            elements[Transformer] = {el['id']: Transformer(from_dict=el) for el in transDicts}
            
            return elements
    


class MATLAB_systemFile(ResultsFile):
    
    def __init__(self, fileName=None):
        if fileName is None:
            fileName = os.path.join(pytreemap.__path__[0], 'sample_results', 'cpfResults_4branches.mat')
        import scipy.io

        self.results = scipy.io.loadmat(fileName, struct_as_record=False)
    
    
    def getBaseLoad(self): 
        """ How to get the base load from cpfResults.mat"""
        return self.results['baseLoad'][0][0]
    
    def CPFloads(self): 
        """ How to get the results of CPF from cpfResults.mat"""
        return self.results['CPFloads'][0]
        
    def getReductions(self):
        """ Get the reduction in loading from the base load and CPF results."""
        return self.baseLoad() - self.CPFloads()
    
    @doneLog('Faults Created', len)
    def buildFaults(self, FaultType, filter = 0):
        """ build a list of faults from cpfFile """
        baseLoad = self.baseLoad
        
        faults = [ FaultType(listing, baseLoad-load) for listing, load in zip(self.faultListings(),self.CPFloads()) if (baseLoad-load)/baseLoad > filter/100]

        
        return faults
    
    
    def faultListings(self):
        """ Create a set of dumb-listings for faults in cpfResults.mat """
        
        elements = self.getElements()
        
        #convert fault listings into simple lists instead of scipy matlab structures
        def collapse(listing):
            """ Convert a matlab fault listings to Python-readable listings, from inscrutable scipy matlab structures. """
            branch, bus, gen, trans = [list(el[0]) if len(el) == 1 else list(el) for el in [listing.branch, listing.bus, listing.gen, listing.trans]]
            
            
            faultEls = [];
            for Type, typelist in zip([Branch, Bus, Gen, Transformer], [branch, bus, gen, trans]):
                faultEls += [elements[Type][id] for id in typelist]
            
            relisting = defaultdict(list)
            relisting['label'], relisting['elements'] = str(listing.label[0]), faultEls
            return relisting
    
        faultListings = (collapse(listing[0][0]) for listing in self.results['branchFaults'][0])
        
        return faultListings
    
    def baseSystem(self):
        return self.results['base'][0,0]
    
    
    @doneLog('Grid Elements Created')
    def buildElements(self):
        base = self.baseSystem()
        
        #get a list of buses attached to each branch
        branchBusEnds = [ [int(el) for el in listing[0:2]] for listing in base.branch]
        nBranches = len(base.branch)
        nBusses = len(base.bus)
        nGens = len(base.gen)
        
        #since numpy isn't that great at loading cell arrays, we need to use try/catch to ensure we don't try to read an empty trans array
        nTrans = len(base.trans[0]) if len(base.trans) > 0 else 0
        
        elements = defaultdict(list)
        
        def getBranchId(busEnds):
            #find the branch index of a branch from the busses it connects to.
            busEnds = set(busEnds)
            mIndex = -1
            for index, branch in enumerate(branchBusEnds):
                mBranch = set(branch)
                intersection = set.intersection(mBranch, busEnds)
                if len( intersection) > 1: return index
            return mIndex

        def getGenId(bus):
            #find the id of a generator given the bus it is in
            try:
                return 1 + [ int(el) for el in base.gen.transpose()[0]].index(bus)
            except ValueError:
                return -1
        
        def defaultIZE(dictionary,default_factory=list):
            newDict = defaultdict(default_factory)
            for k,v in dictionary.items():
                newDict[k]=v
            
            return newDict
            
        def getTransEls(trans):
            transEls = []
            #get branches involved
            transEls += [ elements[Branch][getBranchId(listing)] for listing in (trans[0][0] if len(trans[0]) > 0 else [])]
            #get busses involved
        #     import pdb; pdb.set_trace()
            mBusses = defaultIZE(elements[Bus])
            transEls += [mBusses[id] for id in (trans[0][1][0] if len(trans[0][1]) > 0 else [])]
            #get gens involved
            
            
            transEls += [ mBusses[getGenId(bus)] for bus in ( trans[0][2][0] if len(trans[0][2]) > 0 else [])]
            transEls = [el for el in transEls if el != []]
            return transEls
        
        def negateY(element):
            element = transpose(array(element))
            element = transpose([list(element[0]), list(element[1]*-1)])
            element = [list(point) for point in element]
            return element
        
        
        # build elements
        busIds, busPos = [int(el) for el in base.bus.transpose()[0]], base.bus_geo
        genBusses = [int(el) for el in base.gen.transpose()[0]]
        
        branchPos = [element for element in base.branch_geo[0]] # branchPos = [negateY(element) for element in base.branch_geo[0]]
        
        
        elements[Bus] = {id: Bus(id, list(pos)) for id, pos in  zip(busIds, busPos)}
        
        branch_buses = [ [elements[Bus][key] for key in el] for el in branchBusEnds]
        elements[Branch] ={int(id): Branch(id, list ([ list(point) for point in el]), buses) for id, el, buses in zip(range(1,nBranches+1), branchPos, branch_buses)}#create branches with busses in them, let the branches assign themselves to their busses
        elements[Gen] = {int(id): Gen(id, elements[Bus][bus]) for id, bus in zip(range(1,nGens+1), genBusses)}

        if len(base.trans) > 0: elements[Transformer] = { int(id): Transformer(id, getTransEls(trans)) for id, trans in zip( range(1,nTrans+1), base.trans[0])}
        
        self.elements = elements #save self.elements for later
        
        return self.elements
    
    def boundingRect(self, elList=None):
        
        if not elList:
            elList = self.getElementList()
        
        return boundingRect(elList)
            
#         bounds = array([list(el.boundingRect().getCoords()) for el in elList])
#         boundingRect = [min(bounds[:,0]), min(bounds[:,1]), max(bounds[:,2]), max(bounds[:,3])]
#             
#         return boundingRect
            
   
if __name__ == "__main__":
    main()