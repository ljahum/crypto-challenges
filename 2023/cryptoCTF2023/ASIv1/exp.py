from output import *
 
MR = matrix(GF(3), R)
MS = matrix(GF(3),12100,1, S)
 
a = MR.solve_right(MS)
flag = ''.join([str(a[i,0]) for i in range(110)])
#'12200101122112210002110212001112001011210012200110200221111110001002012120200110211202001221221020201121010111'
bytes.fromhex(hex(int(flag,3))[2:])
b'3Xpl0i7eD_bY_AtT4ck3r!'
 
#CCTF{3Xpl0i7eD_bY_AtT4ck3r!}