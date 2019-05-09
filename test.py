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
import math


filename = "/media/gregory/Acer2/Users/grego/Documents/freelance/img_frame/download.jpeg"
out = "/media/gregory/Acer2/Users/grego/Documents/freelance/img_frame/Output.jpg"
text1 = "Holaaaaarqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq"
text2 = "Buenaaaaaaaaaafeffffffffffffffffffffffffffffffffffffffffffff"

img = Image.open(filename)
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
#text_w, text_h = draw.textsize(text1, font)
#draw.text(((w - text_w ) // 2, h - int(ratio_h*270 )), text1, (0,0,0), font=font)
#text_w, text_h = draw.textsize(text2, font)
#draw.text(((w - text_w - int(ratio_w*150)), h - int(ratio_h*160)), text2, (0,0,0), font=font)

#new_im.save(out)

txt=text1[0]
list_txt=[txt]
idx=0
for i in range(1,len(text1)):
    print(draw.textsize(list_txt[idx]+text1[i], font))
    if(draw.textsize(list_txt[idx]+text1[i], font)[0]>700*ratio_w):
        idx+=1
        list_txt.append(text1[i])
    else:
        list_txt[idx]+=text1[i]
    print(list_txt)
lines1=list_txt
text_1_lines=len(lines1)-1

txt=text2[0]
list_txt=[txt]
idx=0
for i in range(1,len(text2)):
    print(draw.textsize(list_txt[idx]+text2[i], font))
    if(draw.textsize(list_txt[idx]+text2[i], font)[0]>350*ratio_w):
        idx+=1
        list_txt.append(text2[i])
    else:
        list_txt[idx]+=text2[i]
    print(list_txt)
lines2=list_txt
text_2_lines=len(lines2)-1
    

#Extend if necessary :

if text_2_lines+text_1_lines > 0:
    nb=text_2_lines+text_1_lines
    
    top_limit=int(1380*ratio_h)
    central_limit=int(1380*ratio_h+draw.textsize(lines1[0], font)[1]*1.2)
    box_central = (0, top_limit, new_im.size[0], central_limit)
    box_top = (0, 0, new_im.size[0], central_limit)
    box_bottom = (0, central_limit+1, new_im.size[0], new_im.size[1])
    
    central_part = new_im.crop(box_central)
    top_part = new_im.crop(box_top)
    bottom_part = new_im.crop(box_bottom)

    frame = Image.new('RGB', (new_im.size[0],new_im.size[1]+central_part.size[1]*nb))
    offset = (0,0)
    frame.paste(top_part,offset)
    for i in range(0,nb):
        offset = (0,central_limit+i*(central_limit-top_limit))
        frame.paste(central_part,offset)
        
    offset = (0,central_limit+nb*(central_limit-top_limit))
    frame.paste(bottom_part,offset) 
else:
    frame=new_im
#    
draw = ImageDraw.Draw(frame)
    
width_fixed, height_fixed = font.getsize(lines1[0])
# Draw txts
lines = lines1
y_text = h - int(ratio_h*270)
for line in lines:
    width, height = font.getsize(line)
    text_w, text_h = draw.textsize(line, font)
    draw.text(((w - width) / 2, y_text), line, (0,0,0), font=font)
    y_text += height_fixed*1.2

y_text += height_fixed*0.5   
lines = lines2
for line in lines:
    width, height = font.getsize(line)
    text_w, text_h = draw.textsize(line, font)
    draw.text(((w - text_w - int(ratio_w*140)), y_text), line, (0,0,0), font=font)
    y_text += height_fixed*1.2

frame.show()
#frame.save(out)
