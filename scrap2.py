def decorator(func):
    def modify(*args, **kwargs):
        variable = kwargs.pop('variable', "nothing here")
        print(variable)
        x,y = func(*args, **kwargs)
        return x,y
        
    
    return modify

@decorator
def func(a,b):
    print (a**2, b**2)
    return a**2, b**2



func(a=4, b=5, variable="hi")
func(4,5)