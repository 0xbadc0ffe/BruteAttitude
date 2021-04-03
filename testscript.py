import BruteAttitude as BF
import crypt
import hashlib

# Test function, verify if crypt.cyrpt(guess) == hash, where crypt is the DES based hashing function
def test(guess, hash):
    salt = hash[:2]
    hguess = crypt.crypt(guess, salt)
    print(f"[ {hash} ] {guess}                         ", end="\r")
    if hguess == hash:
        print(f"[ {hash} ]  {guess}          ")
        return True
    return False


# Test if the md5 of guess+salt is equal to the hash
def test2(guess, salt, hash):
    print(f"[ {hash} ] {guess}                         ", end="\r")
    if hashlib.md5((guess + salt).encode()).hexdigest() == hash:
        print(f"[ {hash} ]  {guess}          ")
        return True
    return False

# Random test function
def test3(guess):
    if len(guess) == 5:
        if guess.startswith("lol"):
            if guess.endswith("8"):
                print(guess)
                return True    
    return False



dictname = "10-million-password-list-top-1000000.txt"
#charlist = "abcdefghijklmnopqrstuvwxyz0123456789@_-#"
charlist = "abcdefghijklmnopqrstuvwxyz0123456789"
#charlist = "abcdefghijklmnopqrstuvwxyz"
iterset = []
with open(dictname) as file:
    iterset = [guess.strip() for guess in file.readlines()]


psw = "lol"
#hash = "7azfT5tIdyh0I"
hash = crypt.crypt(psw,"ea")
lam = lambda x: test(x,hash)


print(f"### Dictionary attack on {hash}")
input()
if BF.brute_attitude(lam,mode="dictionary", filename=dictname, iterset=iterset):
    pass
else:
    print(f"Failed to recover password from [ {hash} ]")


print(f"\n### Brainless Bruteforce on {hash}")
input()
if BF.brute_attitude(lam, mode="brainless", dim=[1,4], charlist=charlist):
    pass
else:
    print(f"Failed to recover password from [ {hash} ]")


print(f"\n### Masked Dictionary attack on {hash} with default mask")
input()
if BF.brute_attitude(lam,mode="masked-dictionary", filename=dictname, iterset=iterset): #mask="$iter$iter####")
    pass
else:
    print(f"Failed to recover password from [ {hash} ]")


psw = "lollol"
hash = crypt.crypt(psw,"ea")
mask = "$iter1$iter2"

print(f"\n### Multi Dictionary Mask attack {hash} with mask {mask}")
input()
iterset_dict = {    "$iter1": iterset[:100000],     # Only the first 100000 entries of the dictionary
                    "$iter2": iterset[:20]}         # Only the first 20 entries of the dictionary
filename_dict = {   "$iter1": dictname, 
                    "$iter2": dictname}

#if BF.brute_attitude(lam,mode="MDM", filename_dict=filename_dict, mask=mask):
if BF.brute_attitude(lam,mode="MDM", iterset_dict=iterset_dict, mask=mask):
    pass
else:
    print(f"Failed to recover password from [ {hash} ]")




#######

hash = 'f2b31b3a7a7c41093321d0c98c37f5ad'
salt = 'yhbG'   
lam2 = lambda x : test2(x,salt,hash)

print(f"\n### Dictionary attack on {hash}")
input()
if BF.brute_attitude(lam2,mode="dictionary", filename=dictname, iterset=iterset):
    pass
else:
    print(f"Failed to recover password from [ {hash} ]")

print(f"\n### Brainless Bruteforce on {hash}")
input()
if BF.brute_attitude(lam2, mode="brainless", dim=[1,6], charlist="pabcdefghijklmnoqrstuvwxyz"):
    pass
else:
    print(f"Failed to recover password from [ {hash} ]")


##########

print(f"\n### Printing all 4 digits numbers")
input()
BF.brute_attitude(print, mode="brainless", dim=[1,5], charlist="0123456789")

print(f"\n### Test3")
input()
BF.brute_attitude(test3, mode="D", filename=dictname)

print()