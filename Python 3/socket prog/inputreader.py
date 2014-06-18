
"""


"""
def input_int(message, keep_trying, default_value = 0):
    while True:
        try:
           integer = int(input(message))
           return integer
        except ValueError:
            print("ERROR: That was not an integer.")
        
        if not keep_trying:
            break
    return default_value

def input_float(message, keep_trying, default_value = 0):
    while True:
        try:
           integer = float(input(message))
           return integer
        except ValueError:
            print("ERROR: That was not an float.")
        
        if not keep_trying:
            break
    return default_value
