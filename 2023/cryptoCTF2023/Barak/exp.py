p = 73997272456239171124655017039956026551127725934222347
G = GF(p)
d = G(68212800478915688445169020404812347140341674954375635)
D = d/3
c = 1
# Hessian Curve:
# x³ + y³ + 1 = 3Dxy
 
# Weierstrass equivalent
a = -27*D*(D^3 + 8)
b = 54*(D^6 - 20*D^3 - 8)
E2 = EllipticCurve(G, [a, b])
print(E2)
# Elliptic Curve defined by y^2 = x^3 + 44905983883632632311912975168565494049729462391119290*x + 4053170785171018449128623853386306889464200866918538 over Finite Field of size 73997272456239171124655017039956026551127725934222347
 
order = E2.order()
# 73997272456239171124655016995459084401465136460086688