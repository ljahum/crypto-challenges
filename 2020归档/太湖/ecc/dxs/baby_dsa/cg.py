r1 = 10859236269959765735236393779936305217305574331839234502190226708929991582386

r2 = 41960642246379067640524709416001536058292817319109764317369777224426218746518

q = 82302835442112137125891403368151249910268706824854786126600390413622302196443

t1 = []
t2 = []
'''
print(123)
a = 123
b = 9
t1 = 12
t2 = 21
q = 0x101
x = 10
p = 127
print(b**x)





r1 = a**(123*t1*21 % q) % q
r2 = a**(123*t2*12 % q) % q
print(r1, r2)
print(pow(r1, 21, q))
print(pow(r2, 12, q))
'''
for i in range(0, 600):
    t1.append(pow(r1, i, q))

for i in range(0, 600):
    t2.append(pow(r2, i, q))

for i in range(0, 600):
    for j in range(0, 600):
        if(i>1 and j>1):
            if(t1[i]==1 or t2[j]==1):
                print(1,i,j)
        
        if(t1[i] == t2[j]):
            print(i, j)
