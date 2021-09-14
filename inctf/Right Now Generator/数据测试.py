import random, hashlib, os, gmpy2, pickle
from icecream import *
from Crypto.Util.number import *
# f = open('enc.pickle', 'rb')
cip = pickle.load( open('enc.pickle', 'rb'))
print(cip)