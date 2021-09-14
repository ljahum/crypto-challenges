from data import cmp_arr,table1

seq = [0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0] # 这个是输入序列
s='1011101110101111111011111100001100110010111111000100011010111010'
s="0101000001000100010011001010110001111011001011001010011101110010"
seq = [int(i) for i in s]
# seq=seq[::-1]
table3 = [0]*0x4000
table = [0]*0x4000
for i in range(0x4000):    # 初始化table
    table[i] = i


table1_hist = [table1]

for i in range(16):
    for dd in range(4):
        tmp_t1 = [0] * 0x4000
        tmp_t3 = [0] * 0x4000
        table1 = table1_hist[-1]
        for j in range(0x4000):
            tmp_t3[j] = table1[table1[j]]
        for j in range(0x4000):
            tmp_t1[j] = tmp_t3[j]
        table1_hist.append(tmp_t1)



n = 0
for i in range(16):
    data1 = seq[i]
    for dd in range(4):
        cur = data1 & 1# 这个相当于取seq每一个bit，一共 16 * 4 = 64 bit
        data1 >>= 1
        table1 = table1_hist[i * 4 + dd]
        if cur: # 根据每一位的bit位决定是否置换..
            for j in range(0x4000):
                table3[j] = table[table1[j]]
            for j in range(0x4000):
                table[j] = table3[j]
print(table[:20]) # 要找出使得 table == cmp_arr 的 seq
