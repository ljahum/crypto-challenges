import binascii
from sage.all import *
import numpy as np
import sys
import time
from icecream import *
def franklin(n, e, delta, c1, c2):
    """
     Return the indeterminate generator of this polynomial ring
     确定一个未知数
    """
    R = PolynomialRing(Zmod(n), 'X')
    X = R.gen()
    f1 = (X)**e - c1
    f2 = (X + delta)**e - c2
    
    r = gcd(f1, f2)
    # get common divisor in PolynomialRing
    print('========================')
    print(r)
    print(type(r))
    co = r.coefficients()
    print(co)
    return -co[0]//co[1]

def hgcd(a0,a1):
    if a1.degree() <= (a0.degree()//2):
        return np.array([[1,0],[0,1]])

    m = a0.degree()//2
    X = a0.variables()[0] 
    b0 = a0 // X**m
    b1 = a1 // X**m
    
    R = hgcd(b0,b1)
    [d,e] = (R.dot(np.array([a0,a1]).transpose())).transpose()
    ff = d % e
    m = m // 2
    g0 = e // X**m
    g1 = ff // X**m

    S = hgcd(g0,g1)
    q = d // e
    return S.dot(np.array([[0,1],[1,-q]])).dot(R)

def gcd(a0,a1):
    while True:
        print(a0.degree(), end=", ", flush=True)
        if a0 % a1 == 0:
            return a1
        if a0.degree() == a1.degree():
            a1 = a0%a1
        #print(a0.degree())
        R = hgcd(a0,a1)
        # ic(R)
        ic(type(R))
        [b0,b1] = R.dot(np.array([a0,a1]).transpose()).transpose()

        if b0%b1==0:
            return b1
        c = b0 % b1
        a0 = b1
        a1 = c

def test_data():
    c0 = int('61be5676e0f8311dce5d991e841d180c95b9fc15576f2ada0bc619cfb991cddfc51c4dcc5ecd150d7176c835449b5ad085abec38898be02d2749485b68378a8742544ebb8d6dc45b58fb9bac4950426e3383fa31a933718447decc5545a7105dcdd381e82db6acb72f4e335e244242a8e0fbbb940edde3b9e1c329880803931c', 16)
    c1 = int('9d3c9fad495938176c7c4546e9ec0d4277344ac118dc21ba4205a3451e1a7e36ad3f8c2a566b940275cb630c66d95b1f97614c3b55af8609495fc7b2d732fb58a0efdf0756dc917d5eeefc7ca5b4806158ab87f4f447139d1daf4845e18c8c7120392817314fec0f0c1f248eb31af153107bd9823797153e35cb7044b99f26b0', 16)
    delta  = int(binascii.hexlify(b'Jane'), 16) - int(binascii.hexlify(b'Alex'), 16)
    n = 0xa35fe41555b06b23cd769a2aad77cad3a3daa6a76de7591c8b8f281afa5125297fb10541387f8b998d2fd1a76120dd147281ac5208ea52d3ecad1e3e7cab5c0db247ddf87cd8adc3ad13bfb571e26d2e17ffa2429a80b7e9dbdf4054845fd2242ae071fe1a195d28900eda405da3e937ca29dff284e0528c3db510dea9c733bf
    e = 0x3001

    flag = franklin(n, e, delta, c0, c1)
    print('')
    h = hex(int(flag))[2:].rstrip("L")
    h = "0" * (len(h) % 2) + h
    print (binascii.unhexlify(h))

def main():

        
    N = 25898966400928827905718377946331123070958718286581765316565582158865227877882475404853218079499084099440419144196215764927720893687968939899067275095801562867742359933997487928281899714724738097735994026225339488710478292473051567851786254924548138570069406420407124627567648479424564834446192417334669768477661434992797176428220265984651288944265998446714590797833756720922745187467388408600309665467669255896919554072379878017822219455974525233467767926938557154083882126002952139561283708342676308894318951822068027821029295524097544028901807902120777407151278396388621981625398417573347316888458337381776303199529
    e = 1048577
    c1 = 11140520553087800834883326476247582685177207584737264356946559762068509060522907835540767944557089926814767920501376431871780404000550271362410228709616559148950928004959648199391157781102695421411667843970881959939688515679415870087007797819271601359811630724878746762862603629420061133824605384527474682526549557804674160851967543475275374840169790764048711047622418045734436512050742433282306694490346907876574514077395835974083376649624559301087384766644865104383786285302561584731767419571603248493060257358632833957327996996960955767927114473513709882904104552609194519132931270741118197821776138632855021619178
    c2 = 2922817623733019475805146570530296261205732600738503605503192845278422660686627490817081424885152809772315629265930072636690234953045955503581182067349322827011065359648958225896393305011175960879100475146203207801533980643261035226402857047007061320653920746872424363923515091038846823007819033456503365649022294092944985887626605207259444051959239244136999684366533551627508385114998024232490369665950339127904350803268889205463047713233591604324960184727360413931125906144631968128488876241314939855024305076160092193380013725939761970042406866169417457376487954247442308318888399299295082898238584625937490546472
    diff = int(binascii.hexlify(b'Kane'), 16) - int(binascii.hexlify(b'Blex'), 16)
           
    flag = franklin(N, e, diff, c1, c2)

    print(flag)

    h = hex(int(flag))[2:].rstrip("L")
    h = "0" * (len(h) % 2) + h
    print (binascii.unhexlify(h))
    end = time.time()
    

start= time.time()

test_data()
# main()
end = time.time()
print(end - start)

'''
933608312
b'dice{Any_sufficiently_advanced_CTF_challenge_is_indistinguishable_from_computational_number_theory} - Blex'
3882.6192874908447
'''
