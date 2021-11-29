import gmpy2
from Crypto.Util.number import *

flag = b"flag{xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx}"

p = getStrongPrime(2048)
for i in range(1, (p+1)//2):
    s += pow(i, p-2, p)
s = s % p
q = gmpy2.next_prime(s)
n = p*q
e = 0x10001
c = pow(bytes_to_long(flag), e, n)
print(p)
print(c)
#27405107041753266489145388621858169511872996622765267064868542117269875531364939896671662734188734825462948115530667205007939029215517180761866791579330410449202307248373229224662232822180397215721163369151115019770596528704719472424551024516928606584975793350814943997731939996459959720826025110179216477709373849945411483731524831284895024319654509286305913312306154387754998813276562173335189450448233216133842189148761197948559529960144453513191372254902031168755165124218783504740834442379363311489108732216051566953498279198537794620521800773917228002402970358087033504897205021881295154046656335865303621793069
#350559186837488832821747843236518135605207376031858002274245004287622649330215113818719954185397072838014144973032329600905419861908678328971318153205085007743269253957395282420325663132161022100365481003745940818974280988045034204540385744572806102552420428326265541925346702843693366991753468220300070888651732502520797002707248604275755144713421649971492440442052470723153111156457558558362147002004646136522011344261017461901953583462467622428810167107079281190209731251995976003352201766861887320739990258601550606005388872967825179626176714503475557883810543445555390014562686801894528311600623156984829864743222963877167099892926717479789226681810584894066635076755996423203380493776130488170859798745677727810528672150350333480506424506676127108526488370011099147698875070043925524217837379654168009179798131378352623177947753192948012574831777413729910050668759007704596447625484384743880766558428224371417726480372362810572395522725083798926133468409600491925317437998458582723897120786458219630275616949619564099733542766297770682044561605344090394777570973725211713076201846942438883897078408067779325471589907041186423781580046903588316958615443196819133852367565049467076710376395085898875495653237178198379421129086523