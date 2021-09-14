from PIL import Image
from icecream import *
from decimal import *
import numpy as np
import random
getcontext().prec = 20

def f1(x):
    # It is based on logistic map in chaotic systems
    # The parameter r takes the largest legal value
    assert(x>=0)
    assert(x<=1)
    r = 4
    return x*r*(1-x)

def f2(x):
    r = 4
    return x*r*(1-x)
def f3(x):
    r = 4
    return x*r*(1-x)

def encryptImage(path):
    im = Image.open(path)
    size = im.size
    pic  = np.array(im) 
    im.close()
    r1 = Decimal('0.478706063089473894123')
    r2 = Decimal('0.613494245341234672318')
    r3 = Decimal('0.946365754637812381837')
    w,h = size
    for i in range(200):
        r1 = f1(r1)
        r2 = f2(r2)
        r3 = f3(r3)
    const = 10**14

    for x in range(w):
        for y in range(h):
            x1 = int(round(const*r1))%w
            y1 = int(round(const*r2))%h
            
            r1 = f1(r1)
            r2 = f2(r2)
            tmp = pic[y,x]
            pic[y,x] = pic[y1,x1]
            pic[y1,x1] = tmp

    # =========================================================
    print(pic[0])
    input()
    
    
    
    p0 = random.randint(100,104)
    c0 = random.randint(200,204)
    p0 = 102
    c0 = 202
    config = (p0,c0)
    # ic| w: 650, h: 114
    print(pic[0])
    for x in range(w):
        for y in range(h):
            

            
            k = int(round(const*r3))%256
            k = bin(k)[2:].ljust(8,'0')
            k = int(k[p0%8:]+k[:p0%8],2)
            r3 = f3(r3)
            p0 = pic[y,x]
            c0 = k^((k+p0)%256)^c0            
            
            pic[y,x] = c0
    

    return pic,size,config
def outputImage(path,pic,size):
    im = Image.new('P', size,'white')
    pixels = im.load()
    for i in range(im.size[0]):
        for j in range(im.size[1]):
            pixels[i,j] = (int(pic[j][i]))

    im.save(path)


# def decryptImage(pic,size,config):
#     .....
    
enc_img = 'flag_enc.bmp'

out_im = 'enc.bmp'

pic,size,_ = encryptImage(enc_img)
outputImage(out_im,pic,size)



