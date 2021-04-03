import string
from itertools import product



def brute_attitude( test, mode:string="B", iterset=None, filename=None, 
                    iterset_dict=None, filename_dict=None, mask = "$iter", 
                    symb="$iter", charlist=string.printable, dim:list=[1,11]):

    if not callable(test): # make this a type hint
        raise Exception("Test input must be a callable")
    res = False
    if mode == "brainless" or mode == "B":
        res = bruttalo(test, charlist, n1=dim[0], n2=dim[1])
    if mode == "brainless-encoded" or mode == "BE":
        res = bruttalo_enc(test, charlist, n1=dim[0], n2=dim[1])
    elif mode == "dictionary" or mode == "D":
        res = bruttalo_colto(test, iterset=iterset, filename=filename)
    elif mode == "masked-dictionary" or mode == "MD":
        res = bruttalo_colto_mascherato(test, iterset=iterset, filename=filename, mask=mask, symb=symb)
    elif  mode == "multi-dictionary-mask" or mode == "MDM":
        res = bruttalo_bene(test, mask, iterset_dict=iterset_dict, filename_dict=filename_dict)
    return res

# brainless brute force
def bruttalo(test, charlist, n1=1, n2=9):
    for n in range(n1,n2):
        for combo in product(charlist, repeat=n):             
            psw = "".join(i for i in combo)
            if test(psw):
                return True
    return False

# brainless brute force encoded
def bruttalo_enc(test, charlist, n1=1, n2=9):
    for n in range(n1,n2):
        for combo in product(charlist, repeat=n):             
            psw = "".join(i for i in combo)
            if test(psw.encode()):
                return True
    return False

# dictionary attack given a dictionary file or an iterset
def bruttalo_colto(test, iterset:list=None, filename:str=None):
    if not( iterset or filename):
        raise Exception("No dictionary spcified. Pass the filename or the iterset as input.")
    if iterset:
        for guess in iterset:
                if test(guess):
                    return True
        return False
    else:
        with open(filename) as file:
            for guess in file.readlines():
                if test(guess.strip()):
                    return True
    return False


# dictionary atk with mask, given a dictionary file 
def bruttalo_colto_mascherato(test, iterset=None,  filename=None, mask="$iter", symb="$iter"):
    if not iterset:
        if not filename:
            raise Exception("No dictionary spcified. Pass the filename or the iterset as input.")
        with open(filename) as file:
            iterset = [ i.strip() for i in file.readlines() ]
    iterset.insert(0,"")
    splitted = mask.split(symb)
    num = len(splitted) - 1
    for words in product(iterset, repeat=num): 
        guess = ""
        k = 0
        for c in splitted:
            if k < num:
                guess += c + words[k]
                k += 1
            else:
                guess += c 
        if test(guess):
            return True
    return False



def rico_subs(mask, dicts, test, first=True, lv=0):
        if lv >= len(dicts):
            #global K
            #K+=1
            if test(mask.strip()):
                return True
            return False
        key_list = [*dicts] # euqivalent to list(dict) and list(dict.keys()), buf faster for short dicts
        key = key_list[lv]
        iterset = dicts[key]
        #print(iterset)
        if first:
            iterset.insert(0,"")
        first = True
        splitted = mask.split(key)
        num = len(splitted) - 1
        for words in product(iterset, repeat=num): 
            psw = ""
            k = 0
            for c in splitted:
                if k < num:
                    psw += c + words[k]
                    k += 1
                else:
                    psw += c 
            #next_dict = dicts.copy() # TODO too much allocations ...  FASTEEER
            res = rico_subs(psw, dicts, test, first, lv+1)
            if res:
                return True
            first = False            
        

def bruttalo_bene(test, mask, filename_dict=None, iterset_dict=None):
    if iterset_dict == None:
        iterset_dict = {}
        keys = [i for i in filename_dict]
        for key in filename_dict:
            filename = filename_dict[key]
            with open(filename) as file:
                iterset_dict[key] = [i.strip() for i in file.readlines()]
    res = rico_subs(mask, iterset_dict, test)
    if res:
        return res
    else:
        return False
    




# TODO
# a Bruteforce library
# you can use the function in an elastic way passing them the equality function condition
# So the library generates the strings and gives them in input to the function passed
# 
# in the library:
#
# def brute(parameters, test_funct):
# .... # create guess
# if test_funct(guess) == True:
#     ...
#
# In the program
#
# Import Brute
#
# def check_hash(guess, hash):
#   if md5(guess) == hash:
#       return True
#   else return False
#
# ...
# hash = ...
# brute(parameters, lambda x: check_hash(x,hash))
# 
#