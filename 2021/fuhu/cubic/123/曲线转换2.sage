
n = 4
a = (4*n ^ 2+12*n-3)
b = 32*(n+3)
ee = EllipticCurve([0, a, 0, b, 0])
# y2=x3+109x2+224x


def orig(P, N):
    x = P[0]
    y = P[1]
    a = (8*(N+3)-x+y)/(2*(N+3)*(4-x))
    b = (8*(N+3)-x-y)/(2*(N+3)*(4-x))
    c = (-4*(N+3)-(N+2)*x)/((N+3)*(4-x))
    da = denominator(a)
    db = denominator(b)
    dc = denominator(c)
    l = lcm(da, lcm(db, dc))
    return [a*l, b*l, c*l]


g = ee.gens()
print(g[0][0],g[0][1])
# [(-200 : 680 : 1)]
P = ee(g[0][0], g[0][1])
# P = ee(g)
# print(P)
for i in range(1,100):
    x,y,z = orig(i*P, n)
    if(x>0 and y>0 and z>0):
        print(f'x={x}\ny={y}\nz={z}\n')
        print((x/(y+z))+(z/(x+y))+(y/(x+z)))
        print(f'i = {i}')
        break
    
    
        



