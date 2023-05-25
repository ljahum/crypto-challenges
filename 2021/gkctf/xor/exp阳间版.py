
# 初始化第1位的已知数：0
def getab(n,x,lenth):
    a_list=[0]
    b_list=[0]
    # 这里判断512位应该就够了阿。。。。
    mask = 0
    for i in range(lenth):
        # 取第n位
        mask = 2**(i+1)-1
        xi = (x>>i) & 1
        nextA_list=[]
        nextB_list=[]
        
        for ai in range(2):
            for bi in range(2):
                for j in range(len(a_list)):
                    if (ai^bi == xi):
                        nlow = n & mask
                        axbLow = (((ai<<i)+a_list[j])*((bi<<i)+b_list[j]))&mask
                        if(nlow==axbLow):
                            nextA_list.append((ai<<i)+a_list[j])
                            nextB_list.append((bi<<i)+b_list[j])
        # 
        a_list = nextA_list
        b_list = nextB_list

    for a in a_list:
        if(n%a==0):
            return(a,n//a)

lenth = 512

n = 83876349443792695800858107026041183982320923732817788196403038436907852045968678032744364820591254653790102051548732974272946672219653204468640915315703578520430635535892870037920414827506578157530920987388471203455357776260856432484054297100045972527097719870947170053306375598308878558204734888246779716599
x = 4700741767515367755988979759237706359789790281090690245800324350837677624645184526110027943983952690246679445279368999008839183406301475579349891952257846
a,b = getab(n,x,lenth)
from icecream import *
ic(a,b)