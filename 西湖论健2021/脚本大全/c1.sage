#! /usr/bin/sage
from sage.all import *
from sage.groups.generic import bsgs
from Crypto.Util.number import *
n = 13756667493528602443942458926079726080891756071885742491298262702083116395832904976879673307437335487158702205354433181030496791779175581960871506645112683925530870346691030250830485580060422680110855402906373002225906819737721863654459168186318161553302557738746501870133812108810904796796929291592147640914883978535472941607616578979138098141411369145307497718809912787023162115386408719565063704984285881888468852692447964620724771879418493087408052934338721804730678656645774667470259546096294487660517394471262096041928141446611561660161463710592477982613160459457144136748959578109736976905604052519437603633133
e =  29962796858561133879017894773790021500955496832845862605047561223268236371422419248037564613903526652171197478172620186686631172768239959943648048321315358745508409331790232290910562370459676768155603193338457030038661254606834243438351869921694459484559299305577741970104444398713297192237778267691833916131316778668914426503853487491483801124592776054563564891127860919563337062135122968175562177486379037830795904102012548792639302285112888448659336738236754863473406236169484630286628757431625855600201666111080787282946932025351543331350564850182096750419206600487508465618979333417832738039555584974328029753
c =  3030257116580707741895512551171067758094164172551166894906435342860657773422014968105266708355390196844669567120465363879461191192376057025606380798110096544536922775477926444686450572733322673521436695636611786810361034508045081789980893051046506303700427805128726986817793128152262335810253365687364281005712950111841366976469047548203777038361300253260002947547448559539736573565442166142187259400551584838302170717770044687183655128306915261004401807233645785952418823359906437070906543327913572788024861672433969111554264056234527505190413572705811932915623335544019802498194967690041566150740736470066280965739
from sage.all import continued_fraction, Integer
def wiener(e, n):
    m = 12345
    c = pow(m, e, n)
 
    list1 = continued_fraction(Integer(e)/Integer(n))
    conv = list1.convergents()
    
    for i in conv:
        d = int(i.denominator()) # 分母
        m1 = pow(c, d, n)
        if m1 == m:
            return d


d = wiener(e, n)
print(long_to_bytes(pow(c,d,n)))
# DASCTF{520b1904077f4928b769140c49dccb64}