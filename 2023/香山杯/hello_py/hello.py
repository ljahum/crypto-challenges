from java import jboolean ,jclass #line:1
import struct #line:3
import ctypes #line:4
def MX (a ,b ,c ,d ,e ,f ):#line:7
    OOO000O0O0OO00000 =(a .value >>5 ^b .value <<2 )+(b .value >>3 ^a .value <<4 )#line:8
    OOO0OOOOOO0O0OO00 =(c .value ^b .value )+(d [(e &3 )^f .value ]^a .value )#line:9
    return ctypes .c_uint32 (OOO000O0O0OO00000 ^OOO0OOOOOO0O0OO00 )#line:11
def encrypt (OO0OO0O0O0O0O0OO0 ,txt ,key ):#line:14
    O0OOO0OO00O0000OO =0x9e3779b9 #line:15
    OOOO0OOOO00O0OOOO =6 +52 //OO0OO0O0O0O0O0OO0 #line:16
    O00OO00000O0OO00O =ctypes .c_uint32 (0 )#line:18
    OO0OOOO0O0O0O0OO0 =ctypes .c_uint32 (txt [OO0OO0O0O0O0O0OO0 -1 ])#line:19
    OOOOO00000OOOOOOO =ctypes .c_uint32 (0 )#line:20
    while OOOO0OOOO00O0OOOO >0 :#line:22
        O00OO00000O0OO00O .value +=O0OOO0OO00O0000OO #line:23
        OOOOO00000OOOOOOO .value =(O00OO00000O0OO00O .value >>2 )&3 #line:24
        for OO0O0OOO000O0000O in range (OO0OO0O0O0O0O0OO0 -1 ):#line:25
            OOO0OO00O0OO0O000 =ctypes .c_uint32 (txt [OO0O0OOO000O0000O +1 ])#line:26
            txt [OO0O0OOO000O0000O ]=ctypes .c_uint32 (txt [OO0O0OOO000O0000O ]+MX (OO0OOOO0O0O0O0OO0 ,OOO0OO00O0OO0O000 ,O00OO00000O0OO00O ,key ,OO0O0OOO000O0000O ,OOOOO00000OOOOOOO ).value ).value #line:27
            OO0OOOO0O0O0O0OO0 .value =txt [OO0O0OOO000O0000O ]#line:28
        OOO0OO00O0OO0O000 =ctypes .c_uint32 (txt [0 ])#line:29
        txt [OO0OO0O0O0O0O0OO0 -1 ]=ctypes .c_uint32 (txt [OO0OO0O0O0O0O0OO0 -1 ]+MX (OO0OOOO0O0O0O0OO0 ,OOO0OO00O0OO0O000 ,O00OO00000O0OO00O ,key ,OO0OO0O0O0O0O0OO0 -1 ,OOOOO00000OOOOOOO ).value ).value #line:30
        OO0OOOO0O0O0O0OO0 .value =txt [OO0OO0O0O0O0O0OO0 -1 ]#line:31
        OOOO0OOOO00O0OOOO -=1 #line:32
    return txt #line:34

def check (O0000000000O0O0O0 ):#line:63
    print ("checking~~~: "+O0000000000O0O0O0 )#line:64
    O0000000000O0O0O0 =str (O0000000000O0O0O0 )#line:65
    if len (O0000000000O0O0O0 )!=36 :#line:66
        return jboolean (False )#line:67
    O00OO00000OO0OOOO =[]#line:69
    for O0O0OOOOO0OOO0OOO in range (0 ,36 ,4 ):#line:70
        OO0OO0OOO000OO0O0 =O0000000000O0O0O0 [O0O0OOOOO0OOO0OOO :O0O0OOOOO0OOO0OOO +4 ].encode ('latin-1')#line:71
        O00OO00000OO0OOOO .append (OO0OO0OOO000OO0O0 )#line:72
    txt =[]#line:73
    for O0O0OOOOO0OOO0OOO in O00OO00000OO0OOOO :#line:74
        txt .append (struct .unpack ("<I",O0O0OOOOO0OOO0OOO )[0 ])#line:75
    print (txt )#line:77
    OO0OO0OOO000OO0O0 =encrypt (9 ,txt ,[12345678 ,12398712 ,91283904 ,12378192 ])#line:78
    enc =[689085350 ,626885696 ,1894439255 ,1204672445 ,1869189675 ,475967424 ,1932042439 ,1280104741 ,2808893494 ]#line:85
    for O0O0OOOOO0OOO0OOO in range (9 ):#line:86
        if enc [O0O0OOOOO0OOO0OOO ]!=OO0OO0OOO000OO0O0 [O0O0OOOOO0OOO0OOO ]:#line:87
            return jboolean (False )#line:88
    return jboolean (True )#line:90
def sayHello ():#line:92
    print ("hello from py")#line:93
