def method_1(arg1, arg2):
    add = arg1 + arg2
    return add

def method_2(n, arg2):
    for i in range(n):
        if i > arg2: 
            print('yes!')
    
def method_3(x):
    # comments
    print('hello!')
    
class class_name_1(object):
    '''
    A paragraph of descriptions...
    '''
    def __init__(self, x, y):
        '''
        A paragraph of decriptions again...
        '''
        self.x = x
        self.y = y
    