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




def CatNum(txt):
    txt = b2s(txt)
    matchObj = re.findall(r'[0-9]+', txt)
    return matchObj
