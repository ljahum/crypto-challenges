# y^2=x^3+fx+g
# f,g = (-11209/48, 1185157/864)
from fractions import Fraction as Frac

from sympy import sqrt
def is_valid(P):
    if P == O:
        return False
    else:
        return ((-39 * sqrt(65) - 109) / 24 < P[0] <
                (-84 * sqrt(3) - 59) / 12) or (
                    (84 * sqrt(3) - 59) / 12 < P[0] < 95 / 12)
O = ("Inf", "Inf")
def ec_plus(P, Q):  
    if P == O:
        return Q
    if Q == O:
        return P
    R = [None] * 2
    if P[0] == Q[0]:
        if P[1] == -Q[1]:
            R = O
        else:
            s = (3 * P[0]**2 + -Frac(11209, 48)) / (2 * P[1])
            R[0] = s**2 - 2 * P[0]
            R[1] = -P[1] + s * (P[0] - R[0])
    else:
        s = (P[1] - Q[1]) / (P[0] - Q[0])
        R[0] = s**2 - P[0] - Q[0]
        R[1] = -P[1] + s * (P[0] - R[0])
    return tuple(R)



# P = S = (-Frac(191, 12), Frac(65, 2))
# cnt = 1
# while not is_valid(S):
#     S = ec_plus(S, P)
#     cnt += 1
#     print("{}P = ({}, {})".format(cnt, *S))
#     if(cnt == 20):
#         break

f,g = (-11209/48, 1185157/864)
E = EllipticCurve([0, 0, 0, f, g])
P = (-191/12,65/2)
P = E(P)
print(9*P)

# y^2=x^3+fx+g
# f,g = (-11209/48, 1185157/864)
