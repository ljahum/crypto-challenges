from functools import reduce

"""扩展欧几里得"""
def egcd(a, b):
    if 0 == b:
        return 1, 0, a
    x, y, q = egcd(b, a % b)
    x, y = y, (x - a // b * y)
    return x, y, q

"""中国剩余定理"""
def chinese_remainder(pairs):
    mod_list, remainder_list = [p[0] for p in pairs], [p[1] for p in pairs]
    mod_product = reduce(lambda x, y: x * y, mod_list)
    mi_list = [mod_product//x for x in mod_list]
    mi_inverse = [egcd(mi_list[i], mod_list[i])[0] for i in range(len(mi_list))]
    x = 0
    for i in range(len(remainder_list)):
        x += mi_list[i] * mi_inverse[i] * remainder_list[i]
        x %= mod_product
    return x

print(chinese_remainder([(8, 2), (9, 4), (25, 19), (7, 2), (1331, 245), (17, 11), (53, 24), (67, 10), (89, 25), (271, 257), (317, 196)]))

print(bin(5783832125135169394+7740459702534774600)[2:])
print(hex(5783832125135169394))
s="0101000001000100010011001010110001111011001011001010011101110010"
print([int(i) for i in s])
# for i in range(16):
# 	if(int(s[i*4:i*4+4],2)>9):
# 		print(hex(int(s[i*4:i*4+4],2))[2:],end='')
# 	else:
# 		print(int(s[i*4:i*4+4],2),end='')
# print()
# res="50444cac7b2ca772"
# for i in range(16):
# 	print(a[15-i],end='')