from Crypto.Cipher import DES3
ans = [163, 246, 150, 62, 51, 77, 196, 195, 217, 14, 114, 101, 54, 157, 51, 43, 159, 141, 44, 240, 184, 78, 254, 164, 169, 210, 106, 142, 66, 244, 94, 64]
c = bytes(ans)
key = b'WelcomeToTheGKCTF2021XXX'
iv1 = b'1Ssecret'
iv2 = b'wumansgy'

# key = b'00000000'
# iv = b'00000000'
des = DES3.new(key,DES3.MODE_CBC,iv1)



m = des.decrypt(c)

print(m)