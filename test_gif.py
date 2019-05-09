#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 23 16:49:59 2018

@author: gregory
"""

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 
from PIL import ImageChops
import imageio
from PIL import ImageSequence
import numpy as np
import sys

import random


        
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
    #text_w, text_h = draw.textsize(text1, font)
    #draw.text(((w - text_w ) // 2, h - int(ratio_h*270 )), text1, (0,0,0), font=font)
    #text_w, text_h = draw.textsize(text2, font)
    #draw.text(((w - text_w - int(ratio_w*150)), h - int(ratio_h*160)), text2, (0,0,0), font=font)
    
    #new_im.save(out)
    
    txt=text1[0]
    list_txt=[txt]
    idx=0
    for i in range(1,len(text1)):
        #print(draw.textsize(list_txt[idx]+text1[i], font))
        if(draw.textsize(list_txt[idx]+text1[i], font)[0]>1000*ratio_w):
            idx+=1
            list_txt.append(text1[i])
        else:
            list_txt[idx]+=text1[i]
        #print(list_txt)
    lines1=list_txt
    text_1_lines=len(lines1)-1
    
    txt=text2[0]
    list_txt=[txt]
    idx=0
    for i in range(1,len(text2)):
        #print(draw.textsize(list_txt[idx]+text2[i], font))
        if(draw.textsize(list_txt[idx]+text2[i], font)[0]>500*ratio_w):
            idx+=1
            list_txt.append(text2[i])
        else:
            list_txt[idx]+=text2[i]
        #print(list_txt)
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
        
    return frame

filename = "87CZYhSV.gif"
out = "ppout.gif"
text1 = "fezfzef"
text2 = "zfzefef"

img = Image.open(filename)
#frames = [frame.copy() for frame in ImageSequence.Iterator(img)]

gif = { 'frames': [],
        'delay': img.info['duration'],
        'loc' : 0,
        'len' : 0 }

__image = Image.open(filename)
__frames=None
first=True
limit=None


def frame_count():
    if __frames:
        return len(__frames)

    try:
        return __image.n_frames
    except AttributeError:
        return 1



indexes = list(range(frame_count()))
if limit:
    if not first:
        mix = indexes[1:]
        random.shuffle(mix)
        indexes[1:] = mix
    indexes = indexes[:limit]

__frames = [
    frame.copy()
    for index, frame in enumerate(ImageSequence.Iterator(__image))
    if index in set(indexes)
]

alpha = __frames[2].split()[-1]

t1=Image.alpha_composite(__frames[0],__frames[1])

t1=ImageChops.difference(__frames[0],__frames[1])
    


#__frames[0].paste(__frames[1],(0,0))

__frames[0].save("0.png")
__frames[1].save("1.png")

test = Image.open("1.png")

class GIFError(Exception): pass

def get_gif_num_frames(filename):
    frames = []
    with open(filename, 'rb') as f:
        if f.read(6) not in ('GIF87a', 'GIF89a'):
            raise GIFError('not a valid GIF file')
        f.seek(4, 1)
        def skip_color_table(flags):
            if flags & 0x80: f.seek(3 << ((flags & 7) + 1), 1)
        flags = ord(f.read(1))
        f.seek(2, 1)
        skip_color_table(flags)
        while True:
            block = f.read(1)
            if block == ';': break
            if block == '!': f.seek(1, 1)
            elif block == ',':
                frames += 1
                f.seek(8, 1)
                skip_color_table(ord(f.read(1)))
                f.seek(1, 1)
            else: raise GIFError('unknown block type')
            while True:
                l = ord(f.read(1))
                if not l: break
                f.seek(l, 1)
    return frames

frr=get_gif_num_frames(filename)

######## SAVE
def animated():
    return frame_count > 1

options = {'save_all': True, 'append_images': __frames[1:]} \
    if __image.format == 'GIF' and animated() else {}

__frames[0].save("TEST.GIF", __image.format, **options)

if gif['delay']==0:
    gif['delay']=200


new_pics=[]
c=0
temp=frames[0]
for val in frames:
    
    temp.paste(val)
    #newImg(temp).save('sample-out'+str(c)+'.png')
    c+=1
    gif['frames'].append(np.asarray(newImg(temp)))

gif['len'] = len(gif['frames'])


images = []
for frame in gif['frames']:
    images.append(gif['frames'])

frames[0].save('anitest.gif',
               save_all=True,
               append_images=frames[1:],
               duration=200,
               loop=0)

#imageio.mimsave(out, gif['frames'],fps=int(1/(gif['delay']/1000.0)),lol="lol")
