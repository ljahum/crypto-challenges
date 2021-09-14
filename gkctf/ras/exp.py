from libnum import *
from Crypto.Util.number import *
from icecream import *
e = 65537
c=13492392717469817866883431475453770951837476241371989714683737558395769731416522300851917887957945766132864151382877462142018129852703437240533684604508379950293643294877725773675505912622208813435625177696614781601216465807569201380151669942605208425645258372134465547452376467465833013387018542999562042758
n1=75003557379080252219517825998990183226659117019770735080523409561757225883651040882547519748107588719498261922816865626714101556207649929655822889945870341168644508079317582220034374613066751916750036253423990673764234066999306874078424803774652754587494762629397701664706287999727238636073466137405374927829

c1=68111901092027813007099627893896838517426971082877204047110404787823279211508183783468891474661365139933325981191524511345219830693064573462115529345012970089065201176142417462299650761299758078141504126185921304526414911455395289228444974516503526507906721378965227166653195076209418852399008741560796631569
cc1=23552090716381769484990784116875558895715552896983313406764042416318710076256166472426553520240265023978449945974218435787929202289208329156594838420190890104226497263852461928474756025539394996288951828172126419569993301524866753797584032740426259804002564701319538183190684075289055345581960776903740881951
cc2=52723229698530767897979433914470831153268827008372307239630387100752226850798023362444499211944996778363894528759290565718266340188582253307004810850030833752132728256929572703630431232622151200855160886614350000115704689605102500273815157636476901150408355565958834764444192860513855376978491299658773170270
# hint1 = pow(2020 * p1 + q1, 202020, n1)
# hint2 = pow(2021 * p1 + 212121, q1, n1)
a = 2020
e1 = 202020
e2 = 212121
tmp = ((cc2-e2)*a*invmod(a+1,n1))%n1
tmp = pow(tmp,e1,n1)-cc1%n1
q1 = gcd(tmp,n1)
p1 = n1//q1
ic(q1,n1%q1)
phi1 = (p1-1)*(q1-1)
d1 = invmod(e,phi1)
P = pow(c1,d1,n1)


a = 2020
e1 = 202020
e2 = 212121
t = e1*e2
n2=114535923043375970380117920548097404729043079895540320742847840364455024050473125998926311644172960176471193602850427607899191810616953021324742137492746159921284982146320175356395325890407704697018412456350862990849606200323084717352630282539156670636025924425865741196506478163922312894384285889848355244489
c2=67054203666901691181215262587447180910225473339143260100831118313521471029889304176235434129632237116993910316978096018724911531011857469325115308802162172965564951703583450817489247675458024801774590728726471567407812572210421642171456850352167810755440990035255967091145950569246426544351461548548423025004
cc1=25590923416756813543880554963887576960707333607377889401033718419301278802157204881039116350321872162118977797069089653428121479486603744700519830597186045931412652681572060953439655868476311798368015878628002547540835719870081007505735499581449077950263721606955524302365518362434928190394924399683131242077
cc2=104100726926923869566862741238876132366916970864374562947844669556403268955625670105641264367038885706425427864941392601593437305258297198111819227915453081797889565662276003122901139755153002219126366611021736066016741562232998047253335141676203376521742965365133597943669838076210444485458296240951668402513
f1 = cc2 *pow(a,e2,n2)*invmod(pow(a+1,e2,n2),n2)%n2
tmp = (pow(f1,e1,n2)-pow(cc1,e2,n2))%n2
q2 = gcd(tmp,n2)
ic(q2,n2%q2)
p2 = n2//q2
phi2 = (p2-1)*(q2-1)
d2 = invmod(e,phi2)
Q = pow(c2,d2,n2)


e = 65537
c=13492392717469817866883431475453770951837476241371989714683737558395769731416522300851917887957945766132864151382877462142018129852703437240533684604508379950293643294877725773675505912622208813435625177696614781601216465807569201380151669942605208425645258372134465547452376467465833013387018542999562042758
p=P
q=Q
n=p*q
phi = (p-1)*(q-1)
d = invmod(e,phi)
m = pow(c,d,n)
print(long_to_bytes(m))
# GKCTF{f64310b5-d5e6-45cb-ae69-c86600cdf8d8}