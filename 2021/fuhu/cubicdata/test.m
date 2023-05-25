R<x,y,z> := RationalFunctionField(Rationals(),3); 
problem := ((x/(y+z) + y/(x+z) + z/(x+y)) - 6) ; 

Evaluate(problem,[-23, -7, 3]); 
problem*Denominator(problem); 

P2<x,y,z> := ProjectiveSpace(Rationals(),2); 

C := Curve(P2,x^3 - 5*x^2*y - 5*x^2*z - 5*x*y^2 - 9*x*y*z - 5*x*z^2 + y^3 - 5*y^2*z -5*y*z^2 + z^3); 

Pt := C![-23, -7, 3]; 

E,f := EllipticCurve(C); 
 
g := f^-1; 
temp := 0;

for n:= 1 to 200 do 
    nPt_inE:=n*f(Pt);
    nPt_inC:=g(nPt_inE); 
    X := Numerator(nPt_inC[1]); 
    Y := Numerator(nPt_inC[2]); 
    Z := Denominator(nPt_inC[1]); 
    if ((X gt 0) and (Y gt 0)) then 
        if((temp eq 0)) then
            printf "x=%o\n",X; 
            printf "%o\n",n;
        end if;
        temp := temp+1;
    end if;  
end for;    

if Evaluate(problem, [X,Y,Z]) eq 0 then 
    printf "I evaluated the point to the original problem and yes, it worked!\n"; 
else 
    printf "Mmm this cannot happen!\n"; 
end if;
