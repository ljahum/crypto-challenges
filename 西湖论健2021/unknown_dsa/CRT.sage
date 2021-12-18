#! /usr/bin/sage
from gmpy2 import iroot
from icecream import *
from sage.all import *
from sage.groups.generic import bsgs
from Crypto.Util.number import *

uu = [10537190383977432819948602717449313819513015810464463348450662860435011008001132238851729268032889296600248226221086420035262540732157097949791756421026015741477785995033447663038515248071740991264311479066137102975721041822067496462240009190564238288281272874966280, 121723653124334943327337351369224143389428692536182586690052931548156177466437320964701609590004825981378294358781446032392886186351422728173975231719924841105480990927174913175897972732532233, 1440176324831562539183617425199117363244429114385437232965257039323873256269894716229817484088631407074328498896710966713912857642565350306252498754145253802734893404773499918668829576304890397994277568525506501428687843547083479356423917301477033624346211335450]
vv = [168450500310972930707208583777353845862723614274337696968629340838437927919365973736431467737825931894403582133125917579196621697175572833671789075169621831768398654909584273636143519940165648838850012943578686057625415421266321405275952938776845012046586285747, 1921455776649552079281304558665818887261070948261008212148121820969448652705855804423423681848341600084863078530401518931263150887409200101780191600802601105030806253998955929263882382004, 25220695816897075916217095856631009012504127590059436393692101250418226097323331193222730091563032067314889286051745468263446649323295355350101318199942950223572194027189199046045156046295274639977052585768365501640340023356756783359924935106074017605019787]
w = [3912956711, 4013184893, 3260747771]
cu = [2852589223779928796266540600421678790889067284911682578924216186052590393595645322161563386615512475256726384365091711034449682791268994623758937752874750918200961888997082477100811025721898720783666868623498246219677221106227660895519058631965055790709130207760704, 21115849906180139656310664607458425637670520081983248258984166026222898753505008904136688820075720411004158264138659762101873588583686473388951744733936769732617279649797085152057880233721961, 301899179092185964785847705166950181255677272294377823045011205035318463496682788289651177635341894308537787449148199583490117059526971759804426977947952721266880757177055335088777693134693713345640206540670123872210178680306100865355059146219281124303460105424]
cv = [168450500310972930707208583777353845862723614274337696968629340838437927919365973736431467737825931894403582133125917579196621697175572833671789075169621831768398654909584273636143519940165648838850012943578686057625415421266321405275952938776845012046586285747, 1643631850318055151946938381389671039738824953272816402371095118047179758846703070931850238668262625444826564833452294807110544441537830199752050040697440948146092723713661125309994275256, 10949587016016795940445976198460149258144635366996455598605244743540728764635947061037779912661207322820180541114179612916018317600403816027703391110922112311910900034442340387304006761589708943814396303183085858356961537279163175384848010568152485779372842]


ans1 = int(crt(cu,uu))
ans = iroot(ans1,int(7))
print(ans)
print(f'm2={long_to_bytes(int(ans[0]))}')
m2 = 10336852405630488944198347577475266693234960398137850045398990629116544863921454
m1 = 8382905590662478666595114136929713707132131361720892331048437274828529226704174

# =========================

uu = [3246103877570376338979874480058302388590234989573846048429589091918737949572620392050082083210013471538484670450175602957972442230909, 121723653124334943327337351369224143389428692536182586690052931548156177466437320964701609590004825981378294358781446032392886186351422728173975231719924841105480990927174913175897972732532233, 1440176324831562539183617425199117363244429114385437232965257039323873256269894716229817484088631407074328498896710966713912857642565350306252498754145253802734893404773499918668829576304890397994277568525506501428687843547083479356423917301477033624346211335450]
vv = [51893133018606205089677829160555654307824024355546397002081760065608182810917693193575928567213487534685441075575788061525676783, 1921455776649552079281304558665818887261070948261008212148121820969448652705855804423423681848341600084863078530401518931263150887409200101780191600802601105030806253998955929263882382004, 25220695816897075916217095856631009012504127590059436393692101250418226097323331193222730091563032067314889286051745468263446649323295355350101318199942950223572194027189199046045156046295274639977052585768365501640340023356756783359924935106074017605019787]
w = [3912956711, 4013184893, 3260747771]
cu = [2852589223779928796266540600421678790889067284911682578924216186052590393595645322161563386615512475256726384365091711034449682791268994623758937752874750918200961888997082477100811025721898720783666868623498246219677221106227660895519058631965055790709130207760704, 21115849906180139656310664607458425637670520081983248258984166026222898753505008904136688820075720411004158264138659762101873588583686473388951744733936769732617279649797085152057880233721961, 301899179092185964785847705166950181255677272294377823045011205035318463496682788289651177635341894308537787449148199583490117059526971759804426977947952721266880757177055335088777693134693713345640206540670123872210178680306100865355059146219281124303460105424]
cv = [148052450029409767056623510365366602228778431569288407577131980435074529632715014971133452626021226944632282479312378667353792117133452069972334169386837227285924011187035671874758901028719505163887789382835770664218045743465222788859258272826217869877607314144, 1643631850318055151946938381389671039738824953272816402371095118047179758846703070931850238668262625444826564833452294807110544441537830199752050040697440948146092723713661125309994275256, 10949587016016795940445976198460149258144635366996455598605244743540728764635947061037779912661207322820180541114179612916018317600403816027703391110922112311910900034442340387304006761589708943814396303183085858356961537279163175384848010568152485779372842]

ans1 = int(crt(cv,vv))
ans = iroot(ans1,int(7))
print(ans)
print(f'm1={long_to_bytes(ans[0])}')
# m2 = 10336852405630488944198347577475266693234960398137850045398990629116544863921454
# uu2 = [iroot(int(1+w[i]*vv[i]**2),int(2)) for i in range(3)]
# print(uu2)
# print(uu)
