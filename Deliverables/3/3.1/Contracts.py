### Below are a bunch of contract functions I made since I don't know modules well
### These simply take in the argument. If the argument is the correct type, then the function
### passes. Otherwise, it will raise an error.

def integer_contract(data):
    if type(data) is not int:
        raise("The argument is not an integer.")
    else:
        pass

def string_contract(data):
    if type(data) is not str:
        raise("The argument is not a string.")
    else:
        pass

def list_contract(data):
    if type(data) is not list:
        raise("The argument is not a list.")
    else:
        pass

def list_of_three_contract(data):
    if type(data) is not list:
        raise("The argument is not a list of three b/c of type mismatch.")
    elif len(data) != 3:
        raise("The argument is not a list of three b/c of list length.")
    else:
        pass

def whole_number_contract(data):
    if type(data) is not int:
        raise("The argument is not a whole number b/c of type mismatch.")
    elif data < 0:
        raise ("The argument is not a whole number b/c it's negative.")
    else:
        pass

def dict_contract(data):
    if type(data) is not dict:
        raise("The argument is not a dictionary.")
    else:
        pass