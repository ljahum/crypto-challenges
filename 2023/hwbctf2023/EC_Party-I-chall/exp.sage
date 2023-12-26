from Crypto.Util.number import *

a,b,n,C = 138681122158674534796479818810828100269024674330030901179877002756402543027343312824423418859769980312713625658733, 4989541340743108588577899263469059346332852532421276369038720203527706762720292559751463880310075002363945271507040, 762981334990685089884160169295988791471426441106522959345412318178660817286272606245181160960267776171409174142433857335352402619564485470678152764621235882232914864951345067231483720755544188962798600739631026707678945887174897543, (19591102741441427006422487362547101973286873135330241799412389205281057650306427438686318050682578531286702107543065985988634367524715153650482199099194389191525898366546842016339136884277515665890331906261550080128989942048438965, 728465071542637655949094554469510039681717865811604984652385614821789556549826602178972137405550902004858456181137844771163710123158955524137202319902378503104952106036911634918189377295743976966073577013775200078470659428344462772)
E = EllipticCurve(Zmod(n),[a,b])
C = E(C)
order = 762981334990685089884160169295988791471426441106522959345445792076415993922016249232021560266153453470937452118572318136597282436269660557904217923887981072203978473274822142705255987334355747997513083011853917049784914749699536828

# fac ord_p*ord_q
o = order // 8452217
print(C*o)
for i in range(1,10000):
    tt = (order//i)*C

# 399142328555769122684976351600136585680104999923110415867753480206443969280985877697850841401824368944437043138064030332535786936031074694422398245233538680969600520572361311820112559527089421156024161654714350513598626449030622660
# p = GCD(n,kp)

p = 37474009785980474658135106783131904659818035950984079581009709986840194575036321428945132957079423328996508289872067
q = n//p
assert p*q == n
Ep = EllipticCurve(Zmod(p),[a,b])
Eq = EllipticCurve(Zmod(q),[a,b])
#print(Ep.order())
#print(Eq.order())
op = 37474009785980474658135106783131904659818035950984079581012533947688268013671227793391417023914911897089093262951596
oq = order // op
dq = inverse_mod(2,oq)
mq = dq*Eq(C)

print(Ep(C))
R.<x> = PolynomialRing(GF(p))
# x^3+a*x+b = y^2
f = (3*x^2+a)^2-2*x*(4*(x^3+a*x+b))-C[0]*4*(x^3+a*x+b)

for i in (f.roots()):
    print(long_to_bytes(crt([int(i[0]),int(mq[0])],[p,q])))
print('done')

# 3crab1n_s0unds_go0d