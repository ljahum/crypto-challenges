
import re
from rich.progress import track
from rich.traceback import install
install()
# -----------------------------------
def CatData(txt,s1,s2):
    if(type(txt)==bytes):
        txt=txt.decode()
    if(type(s1)==bytes):
        s1=s1.decode()
    if(type(s2)==bytes):
        s2=s2.decode()
    
    s = r'(?<='+s1+').*?(?='+s2+')'
    matchObj = re.findall(s, txt)
    return matchObj

# 选取长度大于n的数字字符
def CatHex(txt,length):
    if(type(txt)==bytes):
        txt=txt.decode()
    matchObj = re.findall(r'[0-9a-fA-F]{'+str(length)+r',}', txt)
    return matchObj


line = b'wqqvfqwefqwv 123122312313 saddvasdvasdv 123123235145vdsfvsv,.,;['
print(CatHex(line,5))
print(CatData(line,'wqqvfqwefqwv',',.,;['))