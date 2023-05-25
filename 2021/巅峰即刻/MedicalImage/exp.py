from PIL import Image
from icecream import *
from decimal import *
import numpy as np
import random
im = Image.open('enc.bmp')
pic  = np.array(im)
p = im.load()
im.save('output.bmp')
