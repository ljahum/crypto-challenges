base=1
end = 2

k1=0xde
k2=0xed
k3=0xbe
k4=  0xef
ans=b''
while base<end:
    tmp = idc.get_wide_byte(base)
    base+=1
    
    ans += bytes([tmp^k1^k2^k3^k4])
    if(tmp==0):
        print(ans)
        ans=b''
        
    