Zx.<x>=ZZ[]
from icecream import *
f = Zx([1,-1,1,1,-1])
n=7
d=5
q=256
p = 3

def mul(f, g):
    return (f * g) % (x ^ n-1)


def bal_mod(f, q):
    g = list(((f[i] + q//2) % q) - q//2 for i in range(n))
    return Zx(g)


def random_poly(d):
    assert d <= n
    result = n*[0]
    for j in range(d):
        while True:
            r = randrange(n)
            if not result[r]:
                break
        result[r] = 1-2*randrange(2)
    return Zx(result)


def inv_mod_prime(f, p):
    T = Zx.change_ring(Integers(p)).quotient(x ^ n-1)
    return Zx(lift(1 / T(f)))


def inv_mod_powerof2(f, q):
    assert q.is_power_of(2)
    g = inv_mod_prime(f, 2)
    while True:
        r = bal_mod(mul(g, f), q)
        if r == 1:
            return g
        g = bal_mod(mul(g, 2 - r), q)
# f = random_poly(5)


Zx.<x>=ZZ[]
f = Zx([-1,0,1,-1,1,0,-1])
g = Zx([1, 1, 0, -1, -1, 1,1])
fp = inv_mod_prime(f, p)
fq = inv_mod_powerof2(f, q)
# h=(3*mul(fq,g))

h = bal_mod((p*mul(fq, g)),q)
# ==============================
m = random_poly(7)
r = random_poly(3)
ic(m)
ic(r)
# =============================
c = bal_mod(mul(h,r)+m,q)
ic(c)


# ic(mul(f,c))
a = bal_mod(mul(f,c),q)
m1 = bal_mod(mul(a,fp),p)
ic(m1)
if(m==m1):
    print("================dec success================")
print("public key")
ic(h)
pub_key_coeffs = h.coefficients()
ic(pub_key_coeffs)
# M = matrix(2*n, 2*n,0)
# for i in range(n):
#     M [i,i]=1
#     # for j in range(n):
#     #     M[i,j+n]=pub_key_coeffs[(j-i)%n]
#     for j in range(n):
#         M[i, n+j] = pub_key_coeffs[j]
#     pub_key_coeffs.insert(0, pub_key_coeffs.pop())
#     M[i+n,i+n]=q
# print(M)
# basis = M.BKZ(block_size=24)
M_h = Matrix(n*2, n*2, 0)
for i in range(n):
    M_h[i, i], M_h[n+i, n+i] = 1, q
    for j in range(n):
        M_h[i, n+j] = pub_key_coeffs[j]
    pub_key_coeffs.insert(0, pub_key_coeffs.pop())

M_r = M_h.BKZ(block_size=24)
t = [i for i in M_r[0]]
print(M_r)
print("f = Zx([-1,0,1,-1,1,0,-1])")
print(t)
