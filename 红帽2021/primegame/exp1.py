'''
M = [
    80260960185991308862233904206310070533990667611589946606122867505419956976171,
    127210612166669937440098469708903225618405881204503139663605609326034899514764,
    186360178378489239360019555208872516895923557828929525429878875918225512971166,
    225321001627212097357564035919404985096695078055324870037864774600825628967482,
    277657303409607584257674154656459195924000370301674371438196861060248384105244,
    297000844888383098784779809484430885883324243241834148304083596811292939014380,
    328063692363312405002199287825630301497469991361288129915249443621480610038009,
    340942741029472675751209085563496509709453734782185827155063370803195952763341,
    363065426053956876789136573439806831974720562089628946045509535722562500188081,
    389906219234236504589839583602940131460157322576695243167328885608693810978037,
    397628552821546031788284866976481005071491904149911534621248760160933669557251,
    418115729169523563213795873608243120399117141324174913328486917994007765693981,
    430002268137029940210248704949846802606196021901113383903617291334026458415238,
    435517219435792978548914327540992832715555899417703687725132714593809971489386,
    445816634674050036737403156155461234669588861822924489511566801569753428925196,
    459728395552222169203258553855093151725069310363221663578223702572833827483180,
    472146579573229247119622639984879073370128462957392372371001752039887754216862,
    476006673323706912851925923936227700248085741335072682402231383534286110106849,
    486870143000003523136729364348591878682677901545106867214896561445453739365505,
    493584608712480022671713045430033257561446779236439588774651853861690675528490,
    496801262478540279019120702773153789961300482567894655561867654179758267817025,
    505947495650660962867352926325259167807382070922044420606608075589355194666475,
    511666785983460201877755690981276626403123717604080991115075395552267140888834,
    519748583077886948223642831481589001894608334341623554432584379082164654601617
]
print(len(M))
S2 = 425985475047781336789963300910446852783032712598571885345660550546372063410589918

n = len(M)
L = matrix.zero(n + 1)

for row, x in enumerate(M):
    L[row, row] = 2
    L[row, -1] = x

L[-1, :] = 1
L[-1, -1] = S

res = L.LLL()
print(res)
print(res[0])
'''
flag_data = [-111, -95, -95, -107, -89, -99, -109, -195, -103, -101, -201, -195, -193, -99, -103, -103, -107, -249, 1, 1, 1, 1, 1, 1, 582]

l1=[]
for i in flag_data:
    l1.append(abs(i))
offset_1 = 249

offset =[]
for i in range(len(l1)):
    offset.append((l1[i]-offset_1)//2)

f = ord('}')
for i in offset:
    print(chr(f+i),end='')


flag_data = [-203, -215, -193, -205, -245, -109, -97, -105, -197, -101, -113, -197, -101, -89, -97, -195, -103, -107, -89, -103, -197, -99, -101, -89, 842]
l1=[]
for i in flag_data:
    l1.append(abs(i))

offset =[]
for i in range(len(l1)):
    offset.append((l1[i]-offset_1)//2)


for i in offset:
    print(chr(f+i),end='')
# flag{715c39c3-1b46-4c23-ƥ8006-27b43eba2446}