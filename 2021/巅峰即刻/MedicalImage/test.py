from PIL import Image
from icecream import *
from decimal import *
import numpy as np
import random


getcontext().prec = 20

def f1(x):
    assert(x>=0)
    assert(x<=1)
    r = 4
    return x*r*(1-x)

def f2(x):
    assert(x>=0)
    assert(x<=1)
    r = 4
    return x*r*(1-x)
def f3(x):
    r = 4
    return x*r*(1-x)
# get data1
im = Image.open('flag_enc.bmp')
size = im.size
pixels = im.load()
w,h = size[0],size[1]

pic=[[0 for _ in range(w)] for __ in range(h)]
for i in range(w):
    for j in range(h):
        pic[j][i]=pixels[i,j]
r1 = Decimal('0.478706063089473894123')
r2 = Decimal('0.613494245341234672318')
r3 = Decimal('0.946365754637812381837')
w,h = size
for i in range(200):
    r1 = f1(r1)
    r2 = f2(r2)
    r3 = f3(r3)
const = 10**14


# 先对 R3 序列打表




p0 = 102
c0 = 202
# print(pic[0])
# input()
for x in range(w):
    for y in range(h):
        k = int(round(const*r3))%256
        k = bin(k)[2:].ljust(8,'0')
        k = int(k[p0%8:]+k[:p0%8],2)
        r3 = f3(r3)
        # print(k)
        # input()
        tmp=pic[y][x]
        p0 = ((tmp^c0^k)-k)%256
        
        c0=tmp
        pic[y][x]=p0
        # =====================
        
        # p0 = pic[y][x]
        # c0 = k^((k+p0)%256)^c0
        # pic[y][x] = c0
# print(pic[0])
XX=[]
YY=[]
X=[]
Y=[]

i=0
for x in range(w):
    for y in range(h):
        i+=1
        
        
        x1 = int(round(const*r1))%w
        y1 = int(round(const*r2))%h
        XX.append(x1)
        YY.append(y1)

        r1 = f1(r1)
        r2 = f2(r2)

i-=1

for x in range(w-1,-1,-1):
    for y in range(h-1,-1,-1):   
        x1 = XX[i]
        y1 = YY[i]
        # ic(x1,y1)
        # ic(x,y)
        # input()
        tmp = pic[y1][x1]
        pic[y1][x1] = pic[y][x]
        pic[y][x] = tmp
        i-=1
# print(i)
# print(pic[0])

im = Image.new('P', size,'white')
flag = im.load()
# print(w,h)
# 650 114
for x in range(w):
    for y in range(h):
        flag[x,y] = pic[y][x]
im.save('output.bmp')