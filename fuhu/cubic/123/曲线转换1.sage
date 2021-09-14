from fractions import Fraction as Frac
from icecream import *

R.<x,y,z> = QQ[]
# n=4
F = x^3 + y^3 + z^3 - 3*x^2*(y+z) - 3*y^2*(z+x) - 3*z^2*(x+y) - 5*x*y*z

# n=6
#   x^3 - 5*x^2*y - 5*x^2*z - 5*x*y^2 - 9*x*y*z - 5*x*z^2 + y^3 - 5*y^2*z -5*y*z^2 + z^3

f, g = WeierstrassForm(F)

f, g = (-11209/48, 1185157/864)
E = EllipticCurve([0, 0, 0, f, g])
P = (-191/12, 65/2)
P = E(P)
print(9*P)

print('===================================')

x9P = 637231263346693346010600868176842100660564986054619857/81086401756297731072425447670017660116155468002441526

y9p = 29400417578654041653688375863673590665042836425148365175935874356653994350305605/6284274674391913738225458829167585075352347781720125288787017561681121629385876

a = x9P
b = y9p

A = [[-95/2, -95/2, 277/12],
     [-91/2,  91/2,      0],
     [-6,       -6,      1]
     ]

B = [
    [a],
    [b],
    [1]
]
B = Matrix(B)
m = Matrix(A)
inv_m = m^(-1)
# print(inv_m)

x = inv_m*B
x1 = x[0][0]
x2 = x[1][0]
x3=x[2][0]

t = lcm(x1.denominator(), lcm(x2.denominator(), x3.denominator()))
print(-x1*t)
print(-x2*t)
print(-x3*t)

'''
154476802108746166441951315019919837485664325669565431700026634898253202035277999
36875131794129999827197811565225474825492979968971970996283137471637224634055579
4373612677928697257861252602371390152816537558161613618621437993378423467772036
'''
