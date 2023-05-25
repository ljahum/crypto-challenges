from Crypto.Util.number import *
from tqdm import *
import traceback


# display matrix picture with 0 and X
def matrix_overview(BB, bound):
    for ii in range(BB.dimensions()[0]):
        a = ('%02d ' % ii)
        for jj in range(BB.dimensions()[1]):
            a += ' ' if BB[ii, jj] == 0 else 'X'
            if BB.dimensions()[0] < 60:
                a += ' '
        if BB[ii, ii] >= bound:
            a += '~'
        print(a)


beta = 0.34
delta = 0.02
amplification = 2048

N = 7194944829894746935571965271122989443610702698015123026500274312320541540511952275333536082176132102091625202863345739074691901574020649953130369453360247690506566827078013306825941200018330639608298539682191482947557146237487451707849833303794107411686130468587672820352641436722348277258977791778239539008852841749667581869688275892813664557078043533743669277649148468667399393518112220602616186358353262921270486781426670131125521444335280904901224934061164334131460273779473387748722008412594372005590209919098686472153912130124772089012962023984089123929555594332030502775588070235834837667605812843128059372243
e = 5872666789397408936685003821802975734744078884385553897196686533187747297681714766542317071546532454504513425295170366015384657690105523240363850101369048640430719519784564240908244756652800934680608667950183962226340288720771217107508516125044088043789281574833079766048266075717484676158307477384862873719462770774288252074344824446884295300603035728339571606659365040029505127532956295163195257002051007447197735267997104725561159289832252522298457628452222155625714679911912616173849423059919537353814530280736653541415686756485413316581322357887750268983241858913704388088485132644523120028234659344174431547087
c = 6601667269134560091452287214083525217696007424340765571114688738279264700361513951309195757650152324371826111195352731779137577044473630747863137747356695892337017953751159248388157498368915463745769509485009626774902347006319659852239932231921393353157319713540010424345134411781723171111939891127671029064626426950125001347122070491553845919803891156107693973027238705710354919725550360159383455222982999904576805089837067774838194257113022653159325313574447189639317397889065351340828031907571541750274329094240472180870714728295651611160552345500801797030280900507979459558944006193012524181456837126192865748097\

Xp = int(N**(delta + beta))
Yp = int(N**beta)
Yq = N//Yp

modulus = e
mm = 5
ss = 0
tt = 3

P.<x, y, z> = PolynomialRing(ZZ)
Q = P.quotient(N - y * z)
pol = x * (N - y) + N
pol = Q(pol).lift()

# x-z-shifts
gg = []
monomials = []
for ii in range(mm + 1):
    for jj in range(mm - ii + 1):
        x_z_shift = z ^ ss * x ^ jj * modulus ^ (mm - ii) * pol ^ ii
        x_z_shift = Q(x_z_shift).lift()
        gg.append(x_z_shift)

# y-z-shifts (selected by Herrman and May)
for ii in range(mm + 1):
    for jj in range(1, tt + 1):
        y_z_shift = z ^ ss * y ^ jj * pol ^ ii * modulus ^ (mm - ii)
        y_z_shift = Q(y_z_shift).lift()
        gg.append(y_z_shift)

# list of monomials
for polynomial in gg:
    for monomial in polynomial.monomials():
        if monomial not in monomials:
            monomials.append(monomial)


print(monomials)
print('N =', N)
print('e =', e)

# construct lattice B
nn = len(monomials)
BB = Matrix(ZZ, nn)
for ii in range(nn):
    for jj in range(0, nn):
        if monomials[jj] in gg[ii].monomials():
            BB[ii, jj] = gg[ii].monomial_coefficient(monomials[jj]) * monomials[jj](Xp, Yp, Yq)

matrix_overview(BB, modulus ^ mm)

det = abs(BB.det())
bound = modulus ^ (mm * nn)
print('Bound check:', det < bound)
print(int(det).bit_length(), int(bound).bit_length())

# LLL
BB = BB.LLL()
print('LLL done')
matrix_overview(BB, modulus ^ mm)

PR.<xp, yp, zp> = PolynomialRing(ZZ)
PRQ = PR.quotient(N - yp * zp)
all_pol = []

for pol1_idx in tqdm(range(nn)):
    pol1 = 0
    for jj in range(nn):
        pol1 += monomials[jj](xp, yp, zp) * BB[pol1_idx, jj] / monomials[jj](Xp, Yp, Yq)
    all_pol.append(pol1)

I = ideal(all_pol[:5])
print(I)
print('GB = I.groebner_basis()')
GB = I.groebner_basis()
print('Groebner basis:')
print(GB)
print('-' * 32)

xv, yv, zv = var("xp,yp,zp")
print('roots:')
res = solve([h_i(xv, yv, zv) for h_i in GB], xv, yv, zv)

PRRR.<w> = PolynomialRing(ZZ)
for part_res in res:
    then_res = PRRR(part_res[1](w))
    p = abs(then_res.coefficients()[0].numerator())
    q = N // p
    assert p * q == N
    print(long_to_bytes(pow(c, inverse(e, (p-1)*(q-1)), N)))
