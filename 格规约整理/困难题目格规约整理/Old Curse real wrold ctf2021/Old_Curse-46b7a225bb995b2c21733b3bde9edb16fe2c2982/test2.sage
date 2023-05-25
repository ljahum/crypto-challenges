from Crypto_tools import *
from itertools import *


def matrix_overview(BB):
    for ii in range(BB.dimensions()[0]):
        a = ('%02d ' % ii)
        for jj in range(BB.dimensions()[1]):
            if BB[ii,jj] == 0:
                a += ' '
            else:
                a += 'X'
            if BB.dimensions()[0] < 60:
                a += ' '
        print(a)


def lattice_attack(pol, e, X, Y, Z, mm, tt):
    polys = []

    # G
    for kk in range(mm + 1):
        for i1 in range(kk, mm + 1):
            i3 = mm - i1
            poly = x ^ (i1 - kk) * z ^ i3 * pol ^ kk * e ^ (mm - kk)
            polys.append(poly)

    # H
    for kk in range(mm + 1):
        i1 = kk
        for i2 in range(kk + 1, i1 + tt + 1):
            i3 = mm - i1
            poly = y ^ (i2 - kk) * z ^ i3 * pol ^ kk * e ^ (mm - kk)
            polys.append(poly)

    polys.sort()
    monomials = []
    for poly in polys:
        monomials += poly.monomials()

    monomials = sorted(set(monomials))
    dims1 = len(polys)
    dims2 = len(monomials)
    M = matrix(QQ, dims1, dims2)

    for ii in range(dims1):
        for jj in range(dims2):
            if monomials[jj] in polys[ii].monomials():
                M[ii, jj] = polys[ii](x * X, y * Y, z * Z).monomial_coefficient(monomials[jj])

    matrix_overview(M)
    print('-' * 32)

    print('bound check:', abs(M.det()) < e ^ (dims1 * mm))
    print(int(M.det()).bit_length(), int(e ^ (dims1 * mm)).bit_length())

    BB = M.LLL()
    print('LLL done')
    print('-' * 32)
    matrix_overview(BB)
    print('-' * 32)
    H = [(i, 0) for i in range(dims1)]
    H = dict(H)
    for j in range(dims2):
        for i in range(dims1):
            H[i] += PR((monomials[j] * BB[i, j]) / monomials[j](X, Y, Z))

    H = list(H.values())
    PQ = PolynomialRing(ZZ, 'xq, yq, zq')
    for i in range(dims1):
        H[i] = PQ(H[i])

    xv, yv, zv = var("xq,yq,zq")
    print(solve([h_i(xv, yv, zv) for h_i in H[1:4]], xv, yv, zv))
    print('-' * 32)


N = 80330528881183983072964816732300543404856810562533626369319300810697262966387144944887576330528743612839739692299784591097332512948890518183519167192046959230085412831864255497489112175176914874596237618253755256608956517757030073479666104923402013469283716999320744856718736837534911809839541660207743594867
e = 78452652317506438607956636739779994986676384637399723342738736371812868831141251164966879331214017314432739387076791674001159059604426825547538902010774841189596518785149221523738464397224366361779781148300651051284198636694801404816891957209985325619623109930150535820404950711233032177848101830061155574970

PR = PolynomialRing(ZZ, 'x, y, z')
x, y, z = PR.gens()

alpha = 0.25
gamma = 0.15
delta = 0.15
beta = log2(e) / log2(N)

X = floor(4 * N ^ (beta + delta - 1))
Y = floor(3 * sqrt(2) * N ^ (0.5 + alpha))
Z = floor(N ^ gamma)

# Target polynomial
pol = x * y - N * x + z
mm = 3
tt = 1

lattice_attack(pol, e, X, Y, Z, mm, tt)

'''
[
[xq == r1, yq == r2, zq == -r1*r2 + 4298479533919222051278424008577823787364263332580438512213525069157290784423146604914451469507153913893839652272765256923591944212821123404914813182473920184304071161320177981959839398079746158378586359732136948418875022137978872858278664265291581144582621441419/3602343035298837553927542062227*r1],
[xq == 0, yq == r3, zq == 0],
[xq == r4, yq == (4298479533919222051278424008577823787364263332580438512213525069157290784423146604914451469507153913893839652272765256923591944212821123404914813182473920184304071161320177981959839398079746158378586359732136948418875022137978872858278664265291581144582621441419/3602343035298837553927542062227), zq == 0]
]
'''

y = 4298479533919222051278424008577823787364263332580438512213525069157290784423146604914451469507153913893839652272765256923591944212821123404914813182473920184304071161320177981959839398079746158378586359732136948418875022137978872858278664265291581144582621441419//3602343035298837553927542062227 + 1
x, z = var('x, z', domain=ZZ)

k1 = 3602343035298837553927542062227
k2 = 4298479533919222051278424008577823787364263332580438512213525069157290784423146604914451469507153913893839652272765256923591944212821123404914813182473920184304071161320177981959839398079746158378586359732136948418875022137978872858278664265291581144582621441419

res = solve([z * k1 == -k1*x*y + k2*x], x, z)
print(res)
print('-' * 32)

x = Integer(res[0].coefficients()[0][0])
z = Integer(res[1].coefficients()[0][0])

assert (x * y - N * x + z) % e == 0
u = (x * y - N * x + z) // e
v = x
w = -z

p_s_q_r = N - y
print('(p-s)(q-r) =', p_s_q_r)
print('-' * 32)

a = 3885193323999136856039629631403237736159969409639584250551518536355997978891524564035346751225719460630697433654700022473218421095180111760606245394708999
b = 944838399254930087523310357339939742097556483183482662977225295067404254966876247970295271959280809100126064366722912020666848894003017117276240476372364
E = EllipticCurve(Zmod(N), [a, b])
stone = E(5316297494616251967087180573684467112077977207314228196651011473838683480275875989908990738740861375687186766156200219641981169308660139151062711296717379891376294785675104640775506724244803337279235747630215478504380272738204733311972022712834357078381541224632797503360732934454187646031643331529389570159, 73177062713968648963738410812785853174528721431172461113561340178691492280271903912043554814810920745154304747328073913103230849027745226637330284520633847773874342467137552022725301429074046921710660867115557994943332628756632246059800601063580017261698262663178072317324978782579376388601713100806653808812)

d = inverse(e, p_s_q_r)
heart = d * stone

factors_list = [
    11,
    13,
    131,
    131,
    227,
    251,
    251,
    831396757,
    1108897087,
    2178767881,
    2253769513,
    2698180579,
    3504974177,
    3752390129,
    3787135097,
    4166580373,
    4192312919,
    505386797752007,
    15743834086867007131,
    14842292277078537617,
    15114820929537893567
 ]

base = 120659691081137900860528439558149439256036479214584879088476613192185895986414329679519081477454257879221194033908435726005914629
assert isPrime(base) == 1
assert base * prod(factors_list) == p_s_q_r
cipher = int(heart[0])

P.<x> = PolynomialRing(Zmod(N))
for num in tqdm(range(2, 12)):
    candidate = list(combinations(factors_list, num))
    for tmp_factors in candidate:
        tmp_pro = prod(tmp_factors) * base
        if 510 < int(tmp_pro).bit_length() < 513:
            for padding_bits in range(0, 264, 8):
                p_r = p_s_q_r//tmp_pro
                if b'rwctf' not in long_to_bytes(p_r ^^ (cipher>>padding_bits)):
                    continue
                else:
                    print('Found the p-r:', p_r)
                    print('-' * 32)
                    print('part flag:', long_to_bytes(p_r ^^ (cipher>>padding_bits)))
                    k = 512 - len('rwctf{tH3_CursE_h4S_bR0KEn_o1GIe') * 8

                    print('random padding bits:', k)
                    print('-' * 32)
                    for guess in tqdm([ord('R'), ord('r'), ord('3')]):
                        p_high = ((p_r >> k) << k) + ((guess ^^ 0xb8 ^^ 0x86)<<(k-8))
                        f = p_high + x
                        res = f.monic().small_roots(X=2 ^ (k-5), beta=0.45, epsilon=0.007)
                        if len(res) > 0:
                            print('found the result:', res)
                            p = p_high + int(res[0])
                            q = N // p
                            assert N == p * q
                            print(long_to_bytes((cipher >> padding_bits) ^^ p))
                            sys.exit()