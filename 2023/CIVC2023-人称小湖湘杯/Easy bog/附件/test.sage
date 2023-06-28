#! /usr/bin/sage
from sage.all import *
from sage.groups.generic import bsgs
from Crypto.Util.number import *

p = 85766816683407427477074053090759168259205489535331001301483049660772943816017
pubkey = [58890813098389592716367918664418237809399998613202441049117852003453550490043, 255886907973292033549191761914277947638378726729170162403000263307778539588, 43666147543837562983744529128391108960442814393989688186615627619841168438881, 2289339843351034938706095739069649849491797527322909177303809837660115875707, 41213482604182795008139260226694469358720652561587117539105919206178583341309, 85123975988270149359269904030278272256150702593339117634318036869051474541673, 38499515653492727036642516425661144597669644770181333309684190745152037999340, 20485509602350760468364550436683434882775269798789922529010411809186809838027, 66201868699675751260618542402171897519442339400362102112029773068389836772496, 5928498980938052035989976608996334019121526162545586177960440867589564370967, 50886730626726574520144515855606763616811548330471900085065588158010347676677, 64024533350992434764550819938965710849249693930938822302806256939206336927327, 38725701074483250591450474606717766666514853596721960873869603150079957176979, 79217343443391443055559755031159399927770013676937883189341106207746097977107, 61550584018851036114215415812034871024308694207855706560554908679054705909070, 18943452821091669663831772224349497605704279324611723330470460453532875854668, 19589987578009659601683539978459498259975975776374959927024576839483511789830, 30455762424330442645213719258885752997650973641135913878741104126501286615202, 58949965807078946897782791856062155685595594220625894016492979510745067947620, 62055731853485887582338078878228949009560282473783423335829652944841334703073, 9968050471897160901950463089357618812125361692340159762344476181267684171496, 82879622776859731032127240994822860125030485017752550449574280896284319539559, 4801338348200265259854446071344823901330707085102509710655971928319789477063, 45731791006706217374257923546738746982354369452894895184784691821888225473116, 67249651561046962535594292263727781436622305014470811080407605464069397278541, 74549581000796086938735007821116567870037873934415647996983670510761843574950, 53927163931460713770577528602376533863752551014779597870421933008696943680646, 56674817179749773825254339411582187056553125580899575215919582277873475282705, 46486618405288541635832334168373891479516241585245833202819962034096805786948, 33438500041468604615663063367413201369385488295864836452725688027946579037027, 67664099966578778667405575319488959391557099474146663546553930271609270514413, 45447815671440655615043306804023843286416205143693188321756314646855229497538, 11725972638697133812198141962081533057131109523301554105107846876476492922863, 64289489702331472745122326714411510149286883423778995697545620572730495023564, 57994575257987111046854716965859364231330618527165005046088441624813910607490, 14668229647185139513680523686559656096579435616501772089580139136432744069528, 17932811002316804580991874481669739042847138206519622106023735880404179858139, 5331195663859739712428554823168168360812478289288952467823046758773036202890, 74552793814948855649083379813894922159371588934498467412076815493098565156965, 44935994020454630627073800850452460158487760266394408710221643505798360283738, 56729956460199305019441584184914729272661532037080935244087594435220086006307, 62039396792619765440106521363503635264208869754554560630026111496679072778122, 2393458745997765849524009470841489934632527663821258015836036776013536950950, 35915327454351624449823951016325751779776476237317012289496757290655725512173, 32606524479615026657452402620774183996842863618201886022072527830448469143354, 63235637104235763521471020678482591762365962539497201272446150774560661623146, 62208964066864651499810642926855154855961192109426476051220581622874074871556, 56823425142073561606336827683244447153122191299012994793162957373419782442861, 60885675233604760515790987357657130734130927344692532134660791434444881730069, 70128263220978378037998154126965802527577393332688627564386146841574995052881, 71018980922731664798406835410011497130959699315348431777949257381109611662531, 12143164079299710577697191074655687226341720767219380493916347970636555672200, 13508918371738967514239962849170666297725816564248068619597724335815422874867, 35455956156846758401498039994914987477656410741995261921339242861566953715810, 69980758495467248406706658186358315365421963514406314839633132920772753269590, 40780609781497584108689952068487274243081363044494223353377248536197342087646, 44867942499383360300066493293729414921480295687316596135570022888723461284905, 82725154870798626926322339306353417520587153667878451856611421219700157524903, 25126631681527477467395254546272084567454410334950820629891182857858739056234, 6951466886617047161399523857762365328179011042304277010521273986635895511090, 76348861623318422648322072872825713398471251831589343473949016976971223635877, 56205107190224957419682681113714452084261733562014707901087589292788540501506, 18117892543394976645523077630904329147251317704285881519049138075260678609853, 44808031105096301006447146332872279574072682041430481888991436113801413524922, 49253422883319286749223459668126849556879848229728760990408851547046135426202, 84189814930926817953967035166781168797567323089104013113646102708978330223462, 47137140069594189485896203757476808738350291684312377044596204628988007490802, 40801572088832002265546622948401731702850273201235765228409527972304470614013, 66031049946459598112632104872606456117378438456948859102185817862671625118362, 81720181560222737179789740743588444616843925127263616533094516919384531350798, 22799062566507850812703708400514738660780510100747243720001217935586864713536, 19636898235593770858368519750634152409107475396982151534080287393055054087250, 29019136605948188309201641456999919579306004440518777086603961225647602320689, 79880698495154758609432245210109366091585969807890967815410904513080769679673, 9333444307040962156247586346311311869921891214405652789959336947220586492578, 5389291816105059661723219597627983160117906098832235782666626188832333763452, 80140247201709476779769310874536378021073864035213177889595402673752593492257, 10265989744904418075184606188771633319731922237097882332727796873595806941649, 28947186543573208323555611612621027283989204690818732739083074045376664847781, 76665830939598023116888796550932971936723367285838797618563918377195976634315]
c = 1381426073179447662111620044316177635969142117258054810267264948634812447218

n = 80
for t in range(20,30):
    L = Matrix(ZZ, n+1, n+1)

    for i in range(n):
        L[i, i] = 2
    for i in range(n):
        L[i, n] = pubkey[i]

    L[-1, :] = 1
    tmp = c+p*t
    L[-1, -1] = c+p*t
    # C = c+kp
    res = L.LLL()
    print('k=',t)
    print("enc = ",tmp)
    print(res[0])  
# (1, 1, 1, 1, -1, 1, -1, 1, 1, 1, 1, 1, 1, 1, 1, 1, -1, 1, -1, -1, -1, 1, -1, -1, 1, -1, 1, 1, -1, -1, -1, -1, 1, 1, 1, -1, -1, -1, -1, 1, -1, 1, -1, 1, -1, -1, -1, -1, -1, -1, -1, 1, -1, -1, 1, 1, 1, 1, -1, -1, 1, -1, -1, 1, -1, 1, 1, -1, -1, 1, -1, -1, 1, -1, -1, -1, 1, 1, 1, 1, 0)

