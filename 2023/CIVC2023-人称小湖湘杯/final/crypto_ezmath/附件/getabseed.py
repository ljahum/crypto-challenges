from Crypto.Util.number import *
def gcd(a,b): 
    if(b==0): 
        return a 
    else: 
        return gcd(b,a%b) 
s = [288530505749272642500730917886204398531, 63547143998110685331032679758907988154, 15151206512028268617888756820805603406, 268092204209244869520724955865278855216, 261067075335188593563542448889694952077, 138067838531633886698552659065694918861, 201319433320428898153580935653793106657]
t = []
for i in range(len(s)-1):
    t.append(s[i]-s[i-1]) 
all_n = []
for i in range(len(s)-3):
    all_n.append(gcd((t[i+1]*t[i-1]-t[i]*t[i]), (t[i+2]*t[i]-t[i+1]*t[i+1]))) 
for i in range(len(all_n)-1):
    tmp = GCD(all_n[i+1],all_n[i])
    print(isPrime(tmp),tmp)
# exit()
all_n=[312769358113056565136009929613710078319]
A_list =[]
B_list =[]
seed_list =[]
N_list =[]
for n in all_n:
    
    a=(s[2]-s[1])*inverse((s[1]-s[0]),n)%n
    ani=inverse(a,n)
    b=(s[1]-a*s[0])%n
    seed = (ani*(s[1]-b))%n
    A_list.append(a)
    B_list.append(b)
    seed_list.append(seed)
    N_list.append(n)
    # plaintext=seed
    # print(long_to_bytes(plaintext))
f = open('data.py',"w+")
print("A_list=",A_list,file=f)
print("B_list=",B_list,file=f)
print("seed_list=",seed_list,file=f)
print("N_list=",N_list,file=f)