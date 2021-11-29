
from gen import *
from tqdm import tqdm
from rich.progress import track
from rich.traceback import install
install()
# -----------------------------------

## Reading input
with open("output.txt", "r") as f:
    c = bytes.fromhex(f.readline())
    c = bytes_to_bits(c)
    public = eval(f.read())

def gf2_rank(rows):
    """
    Find rank of a matrix over GF2.

    The rows of the matrix are given as nonnegative integers, thought
    of as bit-strings.

    This function modifies the input list. Use gf2_rank(rows.copy())
    instead of gf2_rank(rows) to avoid modifying rows.
    """
    rank = 0
    while rows:
        pivot_row = rows.pop()
        if pivot_row:
            rank += 1
            lsb = pivot_row & -pivot_row
            for index, row in enumerate(rows):
                if row & lsb:
                    rows[index] = row ^ pivot_row
    return rank
def is_linear_combination(keys, test_value):
    rows = keys.copy()
    rows.append(test_value)
    n = len(rows)
    return gf2_rank(rows) < n
## Recovering last ln//3 keys
ln = len(public)
keys = []
remaining = []
for v in public:
    if 0 in v:
        keys.append(v[0] + v[1])
    else:
        remaining.append(v)

## Fake search
while len(remaining) > 0:
    remaining2 = []
    for v in remaining:
        if is_linear_combination(keys, v[0]):
            keys.append(v[1])
        elif is_linear_combination(keys, v[1]):
            keys.append(v[0])
        else:
            remaining2.append(v)
    remaining = remaining2
    print(len(remaining))

## End
keystream = recover_keystream(keys, public)

flag = bits_to_bytes(xor(c, keystream))
print(flag)
