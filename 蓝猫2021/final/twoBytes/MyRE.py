import re
line = b'Ai have a 0xbef771793b3B'
# matchObj = re.search(r'\d+', line)
# matchObj = re.findall(r'\h+', line)
# [0-9a-fA-F]+\b[0-9a-fA-F]+\b
# matchObj = re.findall(r'[0-9a-fA-F]+', line)
#  (?<=A).*?(?=B)
def b2s(s):
    if(type(s)==str):
        return s
    else:
        return s.decode()


def CatData(txt,s1,s2):
    
    txt = b2s(txt)
    s1 = b2s(s1)
    s2 = b2s(s2)
    s = r'(?<='+s1+').*?(?='+s2+')'
    matchObj = re.findall(s, txt)
    return matchObj


def CatNum(txt):
    txt = b2s(txt)
    matchObj = re.findall(r'[0-9]+', txt)
    return matchObj

def CatHex(txt):
    txt = b2s(txt)
    matchObj = re.findall(r'[0-9a-fA-F]+', txt)
    return matchObj