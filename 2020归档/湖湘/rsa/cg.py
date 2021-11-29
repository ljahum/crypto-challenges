from gmpy2 import iroot

from Crypto.Util.number import *
n = 45644374572906696918751526371540317432552767574531146725947197073091284249824311652929876880761183040024642912502639494246699284890420348711755152172125722304276541146638287085067604879135037538874624825231963426170448359129554061563687341132377272549120305441316002675552272436786866637426883885955669
e = 41481590714555165448395765336905824124002290841668481529563451625379681482568747653473952507567741287320305714776744069287119560788311144707988486438017581271859974139810844158857833808782692691546769253874942787868189158458052798618813933937987400708792117152522747046613196233766095230599127585735387
c = 25790054143492912038696919999059363251926853333642241274795090550534183356849875749287324824373062006504574906179764092648413976672912657535347328280694667704633525599132436478280986985933339098397197660180557793681265237430974006426519650760258181942099887311223904706872308373765682748061276137390494
d = 52659658879277225906413980847487439922520127766333730341313788358471434855931
# n=27
s=iroot(n,3)
print(s)
a = 35737904741097441606899743970223022009440374545057589385206094087708218682067490640350851907056599849
b = 45644374572906696918751526371540317432552767574531146725947197073091284249824311652929876880761183040024642912502639494246699284890420348711755152172125722304276541146638287085067604879135037538874624825231963426170448359129554061563687341132377272549120305441316002675552272436786866637426883885955669

deita = a*a-4*2*(-11)*b
print(deita)
deita = iroot(deita,2)[0]
t = deita - a
q = t//4
print(q)
for i in range(q-0xffffff,q+0xffffff):
    if n%i==0:
        print('yes')
        print(i)
        input()

