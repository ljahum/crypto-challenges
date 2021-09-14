// 
// For my colleagues in Shell with a lot of love,  (and  with a lot of time now since no commuting, cause COVID) 
// Code is commented to explain how to solve the meme  (https://preview.redd.it/p92108lekoq11.jpg?width=367&format=pjpg&auto=webp&s=e0c84917c3d7e130cad06f9ab5a85634b0c88cfb) 
// 
// x/(y+z) + y/(x+z) + z/(x+y) = 4 
// 
// This is the smallest solution: 
// x=4373612677928697257861252602371390152816537558161613618621437993378423467772036 
// y=36875131794129999827197811565225474825492979968971970996283137471637224634055579 
// z=154476802108746166441951315019919837485664325669565431700026634898253202035277999 
// 
// Paste in the site below to execute this code see this result, also read the comments here to understand.  
// The last part of the prints() after executed shows you the solution above. 
// http://magma.maths.usyd.edu.au/calc/ 
// Eduardo Ruiz Duarte  
// toorandom@gmail.com 
// 
 
 
// First we define our environment for our "problem" 
 
R<x,y,z> := RationalFunctionField(Rationals(),3); 
 
problem := ((x/(y+z) + y/(x+z) + z/(x+y)) - 4) ; 
// first note that we know a point after some computation (-1,4,11) that 
// works but has a negative coordinate, the following function returns 0, which means that  
// (x/(y+z) + y/(x+z) + z/(x+y)) - 4 = 0    (just put the -4 in the other side) 
Evaluate(problem,[-1,4,11]); 
 
// after the previous returned 0 , we know the point fits, we continue. 
 
// we multiply by all the denominators of "problem" to get a polynomials 
problem*Denominator(problem); 
// we obtain a polynomial without denominators x^3 - 3*x^2*y - 3*x^2*z - 3*x*y^2 - 5*x*y*z - 3*x*z^2 + y^3 - 3*y^2*z - 3*y*z^2 + z^3 
// We see is cubic, three variables, and every  term has the same degree (3) , therefore this is a cubic  
// homogeneous curve,  we know there is a point which is not the solution we want 
// the point (-1,4,11) fits in the original "problem" so it should fit in this new curve without denominators too (since no denominator becomes 0) 
 
// We transform this equation to a "curve" in Projecive space of dimension 2 
P2<x,y,z> := ProjectiveSpace(Rationals(),2); 
C := Curve(P2,x^3 - 3*x^2*y - 3*x^2*z - 3*x*y^2 - 5*x*y*z - 3*x*z^2 + y^3 - 3*y^2*z - 3*y*z^2 + z^3); 
 
// fit the point to the curve C (no error is returned) 
Pt := C![-1,4,11]; 
 
// Since all cubic homogeneous curve with at least one point define an elliptc curve, we can transform  
// this curve C to an elliptc curve form and just like in cryptography, we will add this known point (mapped to the corresponded curve) 
// with itself until we get only positive coordinates and go back to C (original Problem) 
 
// Below, E is the curve, f is the map that maps   Points f:C -> E  (C is our original curve without denominators, both curves C,E are equivalent  
// but in E we can "Add points" to get another point of E. 
// and with f^-1 we can return to the point of C which is our original solution 

// 三元曲线和 椭圆曲线的变换,在椭圆曲线上可以实现加法

E,f := EllipticCurve(C); 
// E:ecc ,f:C->E
//g is the inverse g:E->C  , f:C->E     so g(f([-1,4,11]))=[-1,4,11] 
g := f^-1; 
 
// We try adding the known point Pt=[-1,4,11] mapped to E, 2..100 times 
// to see if when mapped back the added point to C gives positive coordinates 
//, this is 2*Pt, 3*Pt, ...., 100*Pt  and then mapping back to C all these. 
for n:= 1 to 100 do 
// we calculate n times the point of C, known [-1,4,11] but mapped (via f) inside E (where we can do the "n times")  
    nPt_inE:=n*f(Pt); 
// we take this point on E back to C via f^-1  (which we renamed as g) 
    nPt_inC:=g(nPt_inE); 
// We obtain each coordinate of this point to see if is our positive solution, 
// here MAGMA scales automatically the point such as Z is one always 1,  
// so it puts the same denominators in X,Y, so numerators of X,Y are our  
//solutions and denominator our Z,  think of  P=(a/c,b/c,1)   then c*P=(a,b,c) 
    X := Numerator(nPt_inC[1]); 
    Y := Numerator(nPt_inC[2]); 
    Z := Denominator(nPt_inC[1]); 
    printf "X=%o\nY=%o\nZ=%o\n",X,Y,Z; 
// We check the condition for our original problem. 
    if ((X gt 0) and (Y gt 0)) then 
        printf("GOT IT!!! x=apple, y=banana, z=pineapple, check the above solution\n"); 
        break; 
    else 
        printf "Nee, some coordinate was negative above, I keep in the loop\n\n"; 
    end if; 
end for;    
 
// We check the solution fits in the original problem 
if Evaluate(problem, [X,Y,Z]) eq 0 then 
    printf "I evaluated the point to the original problem and yes, it worked!\n"; 
else 
    printf "Mmm this cannot happen!\n"; 
end if; 