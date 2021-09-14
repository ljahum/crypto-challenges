import pickle
data = pickle.load(open('enc.pickle', 'rb'))
cip = data['cip']
pbkey = data['pbkey']
print(len(pbkey))


S = cip
M = pbkey

n = len(M)
L = matrix.zero(n + 1)

for row, x in enumerate(M):
    L[row, row] = 2
    L[row, -1] = x

L[-1, :] = 1
L[-1, -1] = S
f = open('LLLdata.txt','a+')
res = L.LLL()
for i in range(144):
    ans = list(res[i])
    
    f.write(str(ans)+'\n')
    print(ans)

# inctf{wr5_m4_b4g?}