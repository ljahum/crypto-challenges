output2 = bytes.fromhex("66def695b20eeae3141ea80240e9bc7138c8fc5aef20532282944ebbbad76a6e17446e92de5512091fe81255eb34a0e22a86a090e25dbbe3141aff0542f5")
M=IntegerModRing(p+1)
p = 10000000000000001119
A=Matrix(M,[[8456637504717104773, 644133729621365327, 7060694052512827322],
[4881556192156233109, 7367516523653099255, 6746795449489230423], 
[24069496990635245, 2569299995974183471, 5990686822681667460]])
b=vector(M,[1,1,1])
ee=A.solve_right(b)
e0, e1, e2 = ZZ(ee[0]), ZZ(ee[1]), ZZ(ee[2])

D0, D1, D2 = [J(C(x, min(f(x).sqrt(0,1)))) for x in (11,22,33)]
assert e0*D0+e1*D1+e2*D2 == Q
otp1 = struct.pack("<QQQQQQ", *[u[0],u[1],u[2],v[0],v[1],v[2]])

uu, vv = e0^2*D0+e1^2*D1+e2^2*D2
otp2 = struct.pack("<QQQQQQ", *[uu[0],uu[1],uu[2],vv[0],vv[1],vv[2]])
otp = otp1+otp2
flag = ""
for i in range(len(output2)):
    flag += chr(otp[i]^^output2[i])
print(flag)
'''
(x^3 + 4986131889746979161*x^2 + 1215277151449350005*x + 9406735202825780999,

    6739280444476523560*x^2 + 4418166319852619578*x + 8255796342084066913, 
    3)
'''