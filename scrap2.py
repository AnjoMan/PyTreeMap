


class doneLog(object):
    def __init__(self, message, reportFunc=None):
        self.message = message
        self.reportFunc = reportFunc
    def __call__(self, f):
        from functools import wraps
        @wraps(f)
        def wrapped(*args, **kwargs):
            out = f(*args, **kwargs)
            print("{}{}".format(self.message, " - {}".format(self.reportFunc(out)) if self.reportFunc else ""))
            return out
        
        return wrapped

# def decorate(message):
#     
#     def decorator(*args, **kwargs):
#         print('starting')
#         print('message')
#         result = func(*args, **kwargs)
#         print('done')
#         return result
#     
#     return decorator



@doneLog('fuck you', lambda x: x*400)
def myFunction(a=1, b=1):
    return a+b



c=myFunction(2,2)

# print(c)