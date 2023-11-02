from Crypto.Util.number import *
from gmpy2 import *

e = 0x10001
n= 28576274811010794362153160897556935178530640825011441539841241257190782139295561904323347128956873569754645071205043238985141474388531008367238218822591
c= 49502875285578675438052554215266678403659290915102322948363030271494959804587081871467110614683972929037615883922743651431683465100061968204901334627149795829429950385848753728500177164800064208215503246868631076011505268371936586645321659884527055007299822625570713613996139223348709621258028349513737798120

N = n<<520
pd = iroot(N,2)[0]

# p=9903795849518410344653281228356828212511322954704897576241431455318827688016096172304465212088056377820722871679622052206029611400487162881140178682146173
# p=9903795849518410344653281228356828212511322954704897576241431455318827688016096172304465212088056377820722871679622052206029611400487162881140178682146527
print(pd)
# 9903795849518410344653281228356828212511322954704897576241431455318827688016096172304465212088056377820722871679622052206029611400487162881140178682146183
p1 = pd - 1000
p2 = next_prime(p1)
pq_list = []
for i in range(100):
    nn = (p1*p2)>>520
    if(nn == n):
        pq_list.append((p1,p2))
    p1 = next_prime(p1)
    p2 = next_prime(p1)        
        
for q,p in pq_list:
    n = p*q
    
    phi = (p-1)*(q-1)
    d = inverse(e,phi)        
    m = pow(c,d,n)
    print(long_to_bytes(m))