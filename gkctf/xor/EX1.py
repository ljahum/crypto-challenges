from tqdm import tqdm
from rich.progress import track
from rich.traceback import install
install()
# -----------------------------------
def get_ab(n,x): 
    a = [0]  
    b = [0] 
    # print(a,b)
    maskx = 1 
    maskn = 2
    for i in tqdm(range(512)):
        xbit = (x & maskx) >> i 
        taa = [] 
        tbb = [] 
        for j in range(len(a)): 
            for aa in range(2): 
                for bb in range(2): 
                    if aa^bb == xbit: 
                        # print(a,b)
                        temp2 = n % maskn 
                        temp1 = (aa*maskn//2+a[j]) * (bb*maskn//2+b[j])%maskn
                        if temp1 == temp2: 
                            taa.append(aa*maskn//2+a[j]) 
                            tbb.append(bb*maskn//2+b[j]) 
        maskx *=2 
        maskn *=2 
        a = taa 
        b = tbb 
    print(len(a))
    for a1 in a: 
        if n%a1 == 0: 
            a=a1 
            b=n//a1 
            return a,b

n1 = 83876349443792695800858107026041183982320923732817788196403038436907852045968678032744364820591254653790102051548732974272946672219653204468640915315703578520430635535892870037920414827506578157530920987388471203455357776260856432484054297100045972527097719870947170053306375598308878558204734888246779716599

x1 = 4700741767515367755988979759237706359789790281090690245800324350837677624645184526110027943983952690246679445279368999008839183406301475579349891952257846
a = get_ab(n1,x1)[0]
print(n1%a)
print(a)

