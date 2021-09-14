# from data import encode
from Crypto.Util.number import *

table = 'abcdefghijklmnopqrstuvwxyz'
table = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13,
         14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]

m=25
for a in range(26):
    for b in range(26):
        print((m*a+b)%26,end=' ')
    print('')