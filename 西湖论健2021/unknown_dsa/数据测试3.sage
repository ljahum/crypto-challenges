
# from sage.all import *
# from sage.groups.generic import bsgs
from Crypto.Util.number import *
from Crypto.PublicKey import DSA
from Crypto.Hash import SHA
from gmpy2 import invert,powmod,iroot
import random
from Crypto.Util.number import *

m1=b'Hello, this is the first message.'

m2=b'YES!! that is the second message.'
n, t, invg, = 85198615386075607567070020969981777827671873654631200472078241980737834438897900146248840279191139156416537108399682874370629888207334506237040017838313558911275073904148451540255705818477581182866269413018263079858680221647341680762989080418039972704759003343616652475438155806858735982352930771244880990190318526933267455248913782297991685041187565140859, 106239950213206316301683907545763916336055243955706210944736472425965200103461421781804731678430116333702099777855279469137219165293725500887590280355973107580745212368937514070059991848948031718253804694621821734957604838125210951711527151265000736896607029198, 60132176395922896902518845244051065417143507550519860211077965501783315971109433544482411208238485135554065241864956361676878220342500208011089383751225437417049893725546176799417188875972677293680033005399883113531193705353404892141811493415079755456185858889801456386910892239869732805273879281094613329645326287205736614546311143635580051444446576104548
r1, s1, s2 = 498841194617327650445431051685964174399227739376, 376599166921876118994132185660203151983500670896, 187705159843973102963593151204361139335048329243
r2, s3  = 620827881415493136309071302986914844220776856282, 674735360250004315267988424435741132047607535029
h1 = bytes_to_long(SHA.new(m1).digest())
h2 = bytes_to_long(SHA.new(m2).digest())

# 解方程
'''
a=1
b=-1
c=-n*t
delta = b**2-4*a*c
print(delta)
print(iroot(delta,2))
p = (-b+iroot(delta,2)[0])//(2*a)

'''


q = 895513916279543445314258868563331268261201605181
p = 95139353880772104939870618145448234251031105153406565833029787299040378395002190438381537974853777890692924407167823818980082672873538133127131356810153012924025270883966172420658777903337576027105954119811495411149092960422055445121097259802686960288258399754185484307350305454788837702363971523085335074839

k = (h1-h2)*inverse(s1-s2,q)
x1 = ((s1*k-h1)*inverse(r1,q))%q
print(x1)
flag=b''
flag+=long_to_bytes(x1)
# b'DASCTF{f11bad18f5297'
x1 = 389668174084597613214310991510959871854822701367
g = inverse(invg,n)
r2 = powmod(g, x1, p) % q
x2 = ((s3*k-h1)*inverse(r2,q))%q
print(x2)
flag+=long_to_bytes(x2)
print(flag)

q = 895513916279543445314258868563331268261201605181
p = 95139353880772104939870618145448234251031105153406565833029787299040378395002190438381537974853777890692924407167823818980082672873538133127131356810153012924025270883966172420658777903337576027105954119811495411149092960422055445121097259802686960288258399754185484307350305454788837702363971523085335074839
# DASCTF{f11bad18f529750fe52c56eed85d001b}