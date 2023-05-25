from Crypto.Util.number import *
from tqdm import tqdm
from rich.progress import track
from rich.traceback import install
install()
# -----------------------------------

size = 2**22
with open("lN.bin","rb") as f:
    data = f.read()

f1 = open("data","w+")


for i in tqdm(range(size)):
    tmp = hex(bytes_to_long(data[i*64:(i+1)*64]))[2:]
    f1.write(tmp+'\n')
