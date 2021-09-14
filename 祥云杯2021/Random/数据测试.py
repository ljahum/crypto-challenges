from Crypto.Util.number import *
import random
# seeds = []
# p=getPrime(512)
# q=getPrime(512)
# for i in range(0,154):
#     seeds.append(random.randint(0,10000))



seeds = [4827, 9522, 552, 880, 7467, 7742, 9425, 4803, 6146, 4366, 1126, 4707, 1138, 2367, 1081, 5577, 4592, 5897, 4565, 2012, 2700, 1331, 9638, 7741, 50, 824, 8321, 7411, 6145, 1271, 7637, 5481, 8474, 2085, 2421, 590, 7733, 9427, 3278, 5361, 1284, 2280, 7001, 8573, 5494, 7431, 2765, 827, 102, 1419, 6528, 735, 5653, 109, 4158, 5877, 5975, 1527, 3027, 9776, 5263, 5211, 1293, 5976, 7759, 3268, 1893, 6546, 4684, 419, 8334, 7621, 1649, 6840, 2975, 8605, 5714, 2709, 1109, 358, 2858, 6868, 2442, 8431, 8316, 5446, 9356, 2817, 2941, 3177, 7388, 4149, 4634, 4316, 5377, 4327, 1774, 6613, 5728, 1751, 8478, 3132, 4680, 3308, 9769, 8341, 1627, 3501, 1046, 2609, 7190, 5706, 3627, 8867, 2458, 607, 642, 5436, 6355, 6326, 1481, 9887, 205, 5511, 537, 8576, 6376, 3619, 6609, 8473, 2139, 3889, 1309, 9878, 2182, 8572, 9275, 5235, 6989, 6592, 4618, 7883, 5702, 3999, 925, 2419, 7838, 3073, 488, 21, 3280, 9915, 3672, 579]

res = [55, 5, 183, 192, 103, 32, 211, 116, 102, 120, 118, 54, 120, 145, 185, 254, 77, 144, 70, 54, 193, 73, 64, 0, 79, 244, 190, 23, 215, 187, 53, 176, 27, 138, 42, 89, 158, 254, 159, 133, 78, 11, 155, 163, 145, 248, 14, 179, 23, 226, 220, 201, 5, 71, 241, 195, 75, 191, 237, 108, 141, 141, 185, 76, 7, 113, 191, 48, 135, 139, 100, 83, 212, 242, 21, 143, 255, 164, 146, 119, 173, 255, 140, 193, 173, 2, 224, 205, 68, 10, 77, 180, 24, 23, 196, 205, 108, 28, 243, 80, 140, 4, 98, 76, 217, 70, 208, 202, 78, 177, 124, 10, 168, 165, 223, 105, 157, 152, 48, 152, 51, 133, 190, 202, 136, 204, 44, 33, 58, 4, 196, 219, 71, 150, 68, 162, 175, 218, 173, 19, 201, 100, 100, 85, 201, 24, 59, 186, 46, 130, 147, 219, 22, 81]

ans = [] 
for i in range(0, 154):
    random.seed(seeds[i])
    rands = []
    for j in range(0,4):
        rands.append(random.randint(0,255))
    print(rands)
    ans.append(res[i] ^ rands[i%4])
print(ans)
# print(bytes(ans))
ans = [53, 51, 55, 50, 48, 48, 55, 52, 50, 54, 49, 54, 49, 49, 57, 54, 49, 53, 52, 52, 48, 53, 54, 52, 48, 53, 48, 52, 49, 49, 48, 55, 51, 54, 54, 53, 57, 49, 57, 48, 49, 56, 51, 49, 57, 52, 48, 53, 50, 57, 54, 54, 55, 50, 51, 48, 55, 54, 48, 52, 49, 50, 54, 54, 54, 49, 48, 56, 57, 51, 49, 53, 56, 54, 55, 56, 48, 57, 50, 56, 52, 53, 52, 53, 48, 50, 51, 50, 53, 48, 56, 55, 57, 51, 50, 55, 57, 53, 56, 53, 49, 54, 51, 51, 48, 52, 57, 49, 56, 56, 48, 55, 54, 53, 54, 57, 52, 54, 49, 52, 55, 53, 55, 53, 50, 56, 48, 48, 54, 51, 50, 48, 56, 49, 54, 56, 56, 49, 54, 52, 53, 55, 51, 52, 54, 55, 53, 53, 50, 50, 55, 48, 53, 55]
print(bytes(ans))
# 5372007426161196154405640504110736659190183194052966723076041266610893158678092845450232508793279585163304918807656946147575280063208168816457346755227057