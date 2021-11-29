两个sb题，还是太年轻了

----

# dsa 

    k = pow(y, x, g) * random.randrange(1, 512) % q

化为源根形式爆破 k 分离出 x 消去 x
# rsa
```python
f1 = pow(233*p+q,123,n)
f2 = pow(p+q,321,n)
# ------------------------
# decode
f3 = pow(f1,321,n)
f4 = pow(f2,123,n)
(f3 - f4 ) = (233^(321)-1)*p mod n 
```
