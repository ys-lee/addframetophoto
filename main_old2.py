#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug  3 13:09:29 2018

@author: gregory
"""

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 
import imageio
from PIL import ImageSequence
import numpy as np
import sys

filename = sys.argv[1]
out = sys.argv[2]
text1 = sys.argv[3]
text2 = sys.argv[4]


def newImg(img):
    new_im = Image.open("frame.jpg")
    
    ratio_w = (img.size[0]*1.0)/885
    ratio_h = (img.size[1]*1.0)/1165
    
    new_im=new_im.resize((int(new_im.size[0]*ratio_w),int(new_im.size[1]*ratio_h)),1)
    
    new_im.paste(img, (int(155*ratio_w),
                          int(133*ratio_h)))
    
    
    w, h = new_im.size
    
    
    font = ImageFont.truetype("arial.ttf", int(70*ratio_h))
    draw = ImageDraw.Draw(new_im)
    w, h = new_im.size
    text_w, text_h = draw.textsize(text1, font)
    draw.text(((w - text_w ) // 2, h - int(ratio_h*270 )), text1, (0,0,0), font=font)
    text_w, text_h = draw.textsize(text2, font)
    draw.text(((w - text_w - int(ratio_w*150)), h - int(ratio_h*160)), text2, (0,0,0), font=font)

    return new_im


img = Image.open(filename)

if(len(filename.split('.gif'))>1):
    # im is your original image
    frames = [frame.copy() for frame in ImageSequence.Iterator(img)]
    
    gif = { 'frames': [],
            'delay': img.info['duration'],
            'loc' : 0,
            'len' : 0 }
    
    
    if gif['delay']==0:
        gif['delay']=200
    
    
    new_pics=[]
    c=0
    temp=frames[0]
    for val in frames:
        
        temp.paste(val)
        newImg(temp).save('sample-out'+str(c)+'.png')
        c+=1
        gif['frames'].append(np.asarray(newImg(temp)))
    
    gif['len'] = len(gif['frames'])
    

    
    imageio.mimsave(out, gif['frames'],fps=int(1/(gif['delay']/1000.0)))
else:
    newImg(img).save(out)