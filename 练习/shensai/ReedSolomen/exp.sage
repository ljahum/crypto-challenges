
K.<x> = GF(2 ^ 8, modulus = 'primitive')
alpha = K([1, 1, 1, 0, 1, 0, 0, 1])
PR.<x> = PolynomialRing(K)


f = PR([1, 1, 1, 0, 1, 0, 0, 1])
index = [42,9,217,152,114,202,233,244,20,125,164,54,161,212,254,157,86,238,158,93,232,223,159,156,236,179,145,141,181,89,16,198]
for each in index:
    print("f(alpha ^ %d) = %s" % (each, str(f(alpha ^ each))))
    
    
