p:=10000000000000001119;
K:=GF(p);
R<x>:=PolynomialRing(K);
f:=x^7+x;
C:=HyperellipticCurve(f);
J:=Jacobian(C);
P0:=Points(C,11)[2];
P1:=Points(C,22)[1];
P2:=Points(C,33)[2];
inf:=PointsAtInfinity(C)[1];
D0:=J![P0,inf];
D1:=J![P1,inf];
D2:=J![P2,inf];

u:=x^3 + 8279968990525893430*x^2 + 1550302165483132214*x + 6507629860866868916;
v:=8477847110799285964*x^2 + 1343483448898642569*x + 1883833843420163421;
Q:=J![u,v];
print Q;

Jext:=BaseExtend(J,2);
Qe:=Jext!Q;
D0e:=Jext!D0;
D1e:=Jext!D1;
D2e:=Jext!D2;
for i:=1 to 3 do
        R:=Random(Jext);
        gen:=WeilPairing(Qe, R, p+1);
        a0:=WeilPairing(D0e, R, p+1);
        a1:=WeilPairing(D1e, R, p+1);
        a2:=WeilPairing(D2e, R, p+1);
        l0:=Log(gen, a0);
        l1:=Log(gen, a1);
        l2:=Log(gen, a2);
        print l0, l1, l2;
end for;





'''


 x^3 + 4986131889746979161*x^2 + 1215277151449350005*x + 9406735202825780999 
 [9350413817117071737*x^2 + 4413307456031713654*x + 6799504737297016313, 
 3260719555523477559*x^2 + 5581833680147381541*x + 1744203657915934206, 
 6739280444476523560*x^2 + 4418166319852619578*x + 8255796342084066913, 
 649586182882929382*x^2 + 5586692543968287465*x + 3200495262702984806]
'''
