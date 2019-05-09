import imageio
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 
import imageio
from PIL import ImageSequence
import numpy as np
import sys


gif = imageio.mimread("pp.gif")
nums = len(gif)

im = Image.fromarray(np.uint8(gif[1]))
im = im.convert('RGB')
im.thumbnail((300, 300))
im.show()