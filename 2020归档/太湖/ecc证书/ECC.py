from secret import flag
import codecs


x1 = int(codecs.encode(flag[:12],'hex'),16)
x2 = int(codecs.encode(flag[12:],'hex'),16)
X = (x1,x2)

k = randrange(1, n-1)

y0 = k*G # get (x1 y1)

KPoint = k*PubKey # get (x2 y2) = kP
Y = (X[0] * KPoint.x() % _p, X[1]*KPoint.y() % _p)  # m + (x2 y2)

print("Y={}".format(Y)) # C 
print("y0={}".format(y0)) # x1 y1
