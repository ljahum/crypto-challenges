# ntru密码算法

选取 n p q d

- n = 109 

- q = 2048

- p = 3

为公开参数



q 最好为2的幂,不能为3的倍数

取多项式 f g

prikey 

- f
- fq*f = 1 mod q
- g

pubkey
$$
h \equiv pg*f_{q}\;mod\;q
$$

### enc

取随机数 r,msg多项式化为m

c = rh+m mod q

### dec

a = f*c= f (rh +m )=fprh + fm  = f  *r *pg fq   mod q

a = rpg + m mod q

m = a mod p 



### 攻击实例

This attack breaks NTRU with n = 7, d = 5, q = 256.
get f and g
`f, g = Zx(t[:n]), Zx(t[n:])`

```python


def convolution(f, g):
    return (f * g) % (x ^ n-1)
Zx.<x> = ZZ[]
n = 7
d = 5
q = 256

h=-82*x^6 + 118*x^5 - 94*x^4 + 108*x^3 + 70*x^2 - 122*x + 5

h3 = ((171)*h) % q
# lift(1/Integers(q)(p)) * h
M = matrix(2*n)
for i in range(n): M[i,i] = q
for i in range(n,2*n): M[i,i] = 1
for i in range(n):
    for j in range(n):
        M[i+n,j] = convolution(h3,x^i)[j]
print(M)
print(M.LLL()[0])
```

LLL、BKZ 等格基约化

## LLL算法的推广

The first variant of LLL is called the deep insertion method

---

### BKZ-LLL

The second variant of LLL is based on the notion of a Korkin–Zolotarev
reduced basis

A KZ-reduced basis is generally much better than an LLL-reduced basis

The block Korkin–Zolotarev variant of the LLL algorithm, which is abbreviated
BKZ-LLL, replaces the swap step in the standard LLL

## LLL的应用

