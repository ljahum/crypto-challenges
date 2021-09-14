from Crypto.Util.number import *
from gmpy2 import *
# from datatest import Ns
from data import Ns
LCM = Ns[0]
print(len(Ns))
for i in range(1,len(Ns)):
    LCM = lcm(Ns[i],LCM)
f = open('./outputdata.py', 'w')
# 清空文件
f.seek(0)
f.truncate()
# 写
f.write('LCM = '+str(LCM))

f.close()
