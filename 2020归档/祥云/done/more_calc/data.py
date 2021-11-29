from gmpy2 import *
p = 31
s1 = 0
s2 = 0
ans = []
# for i in range(1, (p+1)//2): # 6
for i in range(1, p-1):  # 11
    ans.append(i)
    print(i, invert(i, p))
    s1 += i
    s2 += invert(i, p)
    if i == (p-1)//2:
        print('--------------')
        print(s1*s2%p)
        print(s1%p, s2%p)
        print('--------------')

print('-----------------')
s1 %= p
s2 %= p
print(s1, s2)

