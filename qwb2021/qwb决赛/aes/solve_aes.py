from phoenixAES import crack_file, convert_r8faults_file
import IPython
from whitebox import out_table, round_mat, round_table, qword
import fuckpy3
import struct
from finite_field import *
from utils import *


def mix_columns(state):
    return map_columns(mix_column, state)


def mix_column(col):
    """
            multiplication by mat_a is equivalent to polynomial multiplication by
            {03}x^3 + {01}x^2 + {01}x^1 + {02}x^0, modulo x^4 + 1

            See Section 4.3 (Polynomials with Coefficients in GF(2^8))

    """

    mat_a = [[0x02, 0x03, 0x01, 0x01],
             [0x01, 0x02, 0x03, 0x01],
             [0x01, 0x01, 0x02, 0x03],
             [0x03, 0x01, 0x01, 0x02]]

    # matrix multiplication
    c2 = bytearray(4)
    for y in range(4):
        for x in range(4):
            c2[y] ^= ff_mulx(col[x], mat_a[y][x])

    return c2


# Section 5.1.3: MixColumns() Transformation
def inv_mix_columns(state):
    return map_columns(inv_mix_column, state)


def inv_mix_column(col):
    """
            mat_ai represents the multiplcative inverse of mat_a, modulo x^4 + 1, i.e.:
            {0b}x^3 + {0d}x^2 + {09}x^1 + {0e}x^0

            >>> inv_mix_columns(mix_columns(b"ABCDEFGHIJKLMNOP"))
            bytearray(b'ABCDEFGHIJKLMNOP')

    """

    mat_ai = [[0x0e, 0x0b, 0x0d, 0x09],
              [0x09, 0x0e, 0x0b, 0x0d],
              [0x0d, 0x09, 0x0e, 0x0b],
              [0x0b, 0x0d, 0x09, 0x0e]]

    # matrix multiplication
    c2 = bytearray(4)
    for y in range(4):
        for x in range(4):
            c2[y] ^= ff_mulx(col[x], mat_ai[y][x])

    return c2


def sub_bytes(state):
    # apply sub_byte() to each element of the state
    return bytearray(map(sub_byte, state))


def sub_byte(x):
    x = ff_multiplicative_inverse(x)

    # affine transform
    x ^= rotl(x, 1) ^ rotl(x, 2) ^ rotl(x, 3) ^ rotl(x, 4) ^ 0x63

    return x


# Section 5.3.2: InvSubBytes() Transformation
def inv_sub_bytes(state):
    # apply inv_sub_byte() to each element of the state
    return bytearray(map(inv_sub_byte, state))


def inv_sub_byte(x):
    # inverse affine transform
    x = rotl(x, 1) ^ rotl(x, 3) ^ rotl(x, 6) ^ 0x05

    return ff_multiplicative_inverse(x)


def shift_rows(state):
    """
            Section 5.1.2: ShiftRows() Transformation

            !!! FUN FACT ALERT !!!
            Rotating a row by one position to the left is equivalent to polynomial
            multiplication by {01}x^3 + {00}x^2 + {00}x^1 + {00}x^0, modulo x^4 + 1

            >>> shift_rows(b"ABCDefghIJKLmnop")
            bytearray(b'AfKpeJoDInChmBgL')

    """

    s2 = bytearray(4 * 4)
    for i in range(4):
        row = state[i: 4 * 4: 4]
        s2[i: 4 * 4: 4] = row[i:] + row[:i]
    return s2


def inv_shift_rows(state):
    """
            Section 5.3.1: InvShiftRows() Transformation

            >>> inv_shift_rows(b"AfKpeJoDInChmBgL")
            bytearray(b'ABCDefghIJKLmnop')

    """

    return shift_rows(shift_rows(shift_rows(state)))


def fun(s):
    new = ''
    for i in range(4):
        v2 = 0
        for j in range(4):
            v2 ^= out_table[256*(4*i+j)+s[4*i+j]]
        new += hex(v2)[2:].zfill(8).unhex()[::-1].hex()
    print(new)


def fuck(s):
    res = []
    for i in range(4):
        target = s[i*4] + (s[i*4+1] << 8) + (s[i*4+2] << 16) + (s[i*4+3] << 24)
        table1 = dict()
        for byte1 in range(256):
            for byte2 in range(256):
                table1[out_table[256 * (4*i)+byte1] ^
                       out_table[256*(4*i+1)+byte2]] = (byte1, byte2)
        table2 = [0 for _ in range(256*256)]
        for byte3 in range(256):
            for byte4 in range(256):
                tmp = out_table[256 *
                                (4*i+2)+byte3] ^ out_table[256*(4*i+3)+byte4]
                todo = target ^ tmp
                if todo in table1.keys():
                    byte1, byte2 = table1[todo]
                    res += [byte1, byte2, byte3, byte4]
    return res


def aes_dec(s, fault=-1, value=1):
    for i in range(10):
        # print(bin(s[0])[2:].zfill(8))
        v12 = [0 for _ in range(16)]
        for j in range(128):
            v12[j//8] |= ((bin((struct.unpack('Q', bytes(s[8:]))[0]) & round_mat[256*i+1+2*j]).count('1') ^
                          bin((struct.unpack('Q', bytes(s[:8]))[0]) & round_mat[256*i+2*j]).count('1')) & 1) << (j % 8)

        if i == 7 and fault != -1:
            v12[fault] = value

        s = []
        for k in range(4):
            v7 = 0
            for l in range(4):
                v7 ^= round_table[4096*i + 256*(4*k+l) + v12[4*k+l]]
            s += list(map(int, struct.pack('I', v7)))
        # print(3, bytearray(s).hex())

    v12 = [0 for _ in range(16)]
    for m in range(128):
        v12[m//8] |= ((bin((struct.unpack('Q', bytes(s[8:]))[0]) & qword[1+2*m]).count('1') ^
                       bin((struct.unpack('Q', bytes(s[:8]))[0]) & qword[2*m]).count('1')) & 1) << (m % 8)
    return fuck(v12)


print(mix_columns(shift_rows(sub_bytes(bytearray(aes_dec([193, 234, 148, 223, 193, 149, 100,
      69, 120, 0, 1, 243, 36, 148, 114, 254]))))).hex())
for i in range(16):
    print(mix_columns(shift_rows(sub_bytes(bytearray(aes_dec([193, 234, 148, 223, 193, 149, 100,
                                                              69, 120, 0, 1, 243, 36, 148, 114, 254], fault=i, value=0xcc))))).hex())


content = '''7427466d603594faa6791e8dafe3d9b5
7492466d6035c7faa6791e186ee3d9b5
7427326d603594fd32791e8daf52d9b5
3927466d609c94faa679488dafe3d982
74b7466d60351cfaa6791eaabce3d9b5
74278d6d603594f4ee791e8daf11d9b5
3c27466d608994faa679708dafe3d9fc
7437466d6035b6faa6791e2cf6e3d9b5
1927466d601994faa6795b8dafe3d9d3
74270a6d603594f06f791e8dafbfd9b5
74272a6d603594e253791e8dafabd9b5
742746fc343594faa62a1e8dafe33fb5
74b5466d60351efaa6791e1832e3d9b5
74274656473594faa68b1e8dafe31eb5
7427464a6f3594faa6f91e8dafe362b5
7427466c7b3594faa6f11e8dafe362b5
a827466d603994faa6792a8dafe3d99c
'''
with open('tracefile1', 'wb') as t:
    t.write(content.encode('utf8'))
# convert_r8faults_file("tracefile1", "tracefile")
print(crack_file('tracefile1', encrypt=False,
                 verbose=10))
