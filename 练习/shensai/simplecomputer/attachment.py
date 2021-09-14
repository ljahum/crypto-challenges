# using python 3.8.8
# This is a simple computer with over 2**100 GB Memory

from hashlib import md5
from secret import flag
import random

simple_list1 = [i for i in range(2 ** 32)]
simple_list2 = [i for i in range(2 ** 64)]
simple_list3 = [i for i in range(2 ** 128)]

choices = []
for i in range(100):
    choices.append(random.choice(simple_list1))
    choices.append(random.choice(simple_list2))
    choices.append(random.choice(simple_list3))

print(choices[:-1])

assert flag.startswith("DASFLAG{") and flag.endswith("}")
assert flag[8:-1] == md5(str(choices[-1]).encode()).hexdigest()