from Crypto.Util.number import *
enc = [
909619317,
912378641,
761422938,
841844503,
1701111746,
1701194992,
959752815,
892545567,
1667598316,]
T = [0,3180180532,86337434,1850726346,2970464585,3350124366]
print(len(enc),len(T))
for i in enc:
    tmp = long_to_bytes(i)
    print(len(tmp),tmp)
    
for i in range(6):
    tpm = enc[i]^(T[i]>>16)
    print(long_to_bytes(tpm))
    