
s = '9894b94f1ba310e39412757481329907'
s = bytes.fromhex(s)
iv = list(s)

s1 = b'name:ljaaa'
s2 = b'name:admin'

ans=[]
for i in range(len(s1)):
    ans.append(s1[i]^s2[i]^iv[i])
s=(ans+iv[len(s1):])

print(bytes(s).hex())
