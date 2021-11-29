#! /usr/bin/sage
from time import time
from sage.all import *
from sage.groups.generic import bsgs
from Crypto.Util.number import *
import itertools

from tqdm import tqdm
from rich.progress import track
from rich.traceback import install
install()
from time import *
p1 = time()

# -----------------------------------
def add(P, Q, mod):
    m, n = P
    p, q = Q

    if p is None:
        return P
    if m is None:
        return Q

    if n is None and q is None:
        x = m * p % mod
        y = (m + p) % mod
        return (x, y)

    if n is None and q is not None:
        m, n, p, q = p, q, m, n

    if q is None:
        if (n + p) % mod != 0:
            x = (m * p + 2) * inverse(n + p, mod) % mod
            y = (m + n * p) * inverse(n + p, mod) % mod
            return (x, y)
        elif (m - n ** 2) % mod != 0:
            x = (m * p + 2) * inverse(m - n ** 2, mod) % mod
            return (x, None)
        else:
            return (None, None)
    else:
        if (m + p + n * q) % mod != 0:
            x = (m * p + (n + q) * 2) * inverse(m + p + n * q, mod) % mod
            y = (n * p + m * q + 2) * inverse(m + p + n * q, mod) % mod
            return (x, y)
        elif (n * p + m * q + 2) % mod != 0:
            x = (m * p + (n + q) * 2) * inverse(n * p + m * q + 2, mod) % mod
            return (x, None)
        else:
            return (None, None)


def power_mul(P, a, mod):
    res = (None, None)
    t = P
    while a > 0:
        if a % 2:
            res = add(res, t, mod)
        t = add(t, t, mod)
        a >>= 1
    return res


def small_roots(f, bounds, m=1, d=None):
	if not d:
		d = f.degree()

	R = f.base_ring()
	N = R.cardinality()
	
	f /= f.coefficients().pop(0)
	f = f.change_ring(ZZ)

	G = Sequence([], f.parent())
	for i in range(m+1):
		base = N^(m-i) * f^i
		for shifts in itertools.product(range(d), repeat=f.nvariables()):
			g = base * prod(map(power, f.variables(), shifts))
			G.append(g)

	B, monomials = G.coefficient_matrix()
	monomials = vector(monomials)

	factors = [monomial(*bounds) for monomial in monomials]
	for i, factor in enumerate(factors):
		B.rescale_col(i, factor)

	B = B.dense_matrix().LLL()

	B = B.change_ring(QQ)
	for i, factor in enumerate(factors):
		B.rescale_col(i, 1/factor)

	H = Sequence([], f.parent().change_ring(QQ))
	for h in filter(None, B*monomials):
		H.append(h)
		I = H.ideal()
		if I.dimension() == -1:
			H.pop()
		elif I.dimension() == 0:
			roots = []
			for root in I.variety(ring=ZZ):
				root = tuple(R(root[var]) for var in f.variables())
				roots.append(root)
			return roots

	return []
N= int(144256630216944187431924086433849812983170198570608223980477643981288411926131676443308287340096924135462056948517281752227869929565308903867074862500573343002983355175153511114217974621808611898769986483079574834711126000758573854535492719555861644441486111787481991437034260519794550956436261351981910433997)
e= int(3707368479220744733571726540750753259445405727899482801808488969163282955043784626015661045208791445735104324971078077159704483273669299425140997283764223932182226369662807288034870448194924788578324330400316512624353654098480234449948104235411615925382583281250119023549314211844514770152528313431629816760072652712779256593182979385499602121142246388146708842518881888087812525877628088241817693653010042696818501996803568328076434256134092327939489753162277188254738521227525878768762350427661065365503303990620895441197813594863830379759714354078526269966835756517333300191015795169546996325254857519128137848289)


R = Integers(e)
PR.<p_q, k> = PolynomialRing(R)
f = k * (N**2 + N*p_q + p_q**2 - N + p_q + 1) + 1
bounds = (2**513, 2**400)
print("strating LLL")
p_q, k = small_roots(f, bounds, m=3, d=4)[0]

p_q = 24061328198598730023892644418337616625129173971437927448877972244319015467758683782803490794256724311673381106878622466514439272631375460573992290498030162
k = 245962077700976781389651438762467784060458007726399012831680541230865888041508191613184353923990248850900264645309752826
print(p_q,k)
E = 123436198430194873732325455542939262925442894550254585187959633871500308906724541691939878155254576256828668497797665133666948295292931357138084736429120687210965244607624309318401630252879390876690703745923686523066858970889657405936739693579856446294147129278925763917931193355009144768735837045099705643710, 47541273409968525787215157367345217799670962322365266620205138560673682435124261201490399745911107194221278578548027762350505803895402642361588218984675152068555850664489960683700557733290322575811666851008831807845676036420822212108895321189197516787046785751929952668898176501871898974249100844515501819117

PR.<x> = PolynomialRing(ZZ)
f = x**2 - int(p_q) * x + N
(p, _), (q, _) = f.roots()
phi = (p ** 2 + p + 1) * (q ** 2 + q + 1)
d = int(pow(e, -1, phi))
tmp = power_mul(E, d, N)

flag1 = long_to_bytes(tmp[0])[:35].decode()
flag2 = long_to_bytes(tmp[1])[:36].decode()

print(flag1+flag2 )
# [(245962077700976781389651438762467784060458007726399012831680541230865888041508191613184353923990248850900264645309752826, 24061328198598730023892644418337616625129173971437927448877972244319015467758683782803490794256724311673381106878622466514439272631375460573992290498030162)]
# pbctf{I_love_to_read_crypto_papers_and_implement_the_attacks_from_them}

p2 = time()
print(p2-p1)