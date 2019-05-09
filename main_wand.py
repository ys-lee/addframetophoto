#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug  3 13:09:29 2018

@author: gregory
"""

#from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 
from PIL import Image as pil_image
from wand.image import Image as wand_image
import imageio
from PIL import ImageSequence
import numpy as np
import sys

filename = sys.argv[1]
out = sys.argv[2]
text1 = sys.argv[3]
text2 = sys.argv[4]

def newImg(img):
    
    new_im = pil_image.open("frame.jpg")
    ratio_w = (img.size[0]*1.0)/885
    ratio_h = (img.size[1]*1.0)/1165
    
    new_im=new_im.resize((int(new_im.size[0]*ratio_w),int(new_im.size[1]*ratio_h)),1).convert('RGBA')
    
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
    
        frame = pil_image.new('RGB', (new_im.size[0],new_im.size[1]+central_part.size[1]*nb))
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



if(len(filename.split('.gif'))>1):
    # im is your original image
    


    frame_info=[]
    src_image=wand_image(filename=filename)
    i=0
    for frame in src_image.sequence:
        with wand_image() as dst_image:
            print(frame.container)
            dst_image.sequence.append(frame)
            print(frame.delay)
            frame_info.append({'left':frame.page_x,'top':frame.page_y,'height':frame.height,'width':frame.width})
            dst_image.save(filename="temp/ol%d.png" % i)
            print(dst_image.height)
            i+=1
            
    img=wand_image(width=frame_info[0]['width'], height=frame_info[0]['height'])
    img.save(filename='background.png')
            
    for j in range(0,i):
        with wand_image(filename='background.png') as bg_img:
            with wand_image(filename="temp/ol%d.png" % j) as fg_img:
                bg_img.composite(fg_img, left=frame_info[j]['left'], top=frame_info[j]['top'])
            bg_img.save(filename='temp/lol%d.png' % (j))
        
    img = pil_image.open(filename)
   
    def checkEqual(lst):
       return lst[1:] == lst[:-1]
   
    frames=[]
    for i in range(0,len(frame_info)):
        frames.append(pil_image.open("temp/lol%d.png" % i).copy())
#    
    gif = { 'frames': [],
            'delay': img.info['duration'] if 'duration' in img.info else 100,
            'loc' : 0,
            'len' : 0 }
    
    
    if gif['delay']==0:
        gif['delay']=200
    

    frames_corrected=[]
    frames_corrected.append(frames[0].convert('RGBA'))
    for i in range(1,len(frames)):
        if(checkEqual(frame_info)):
            frames_corrected.append(frames[i].convert('RGBA'))
        else:
            t=frames[i].convert('RGBA').split()
            if(np.sum(np.asarray(t[2]))+np.sum(np.asarray(t[0]))+np.sum(np.asarray(t[1]))==0):
                frames_corrected.append(frames_corrected[i-1])
            else:    
                frames_corrected.append(pil_image.alpha_composite(frames_corrected[i-1].convert('RGBA'), frames[i].convert('RGBA')))
        
    frames=frames_corrected
    new_pics=[]
    c=0
    temp=frames[0]

    for val in frames:

        
        temp.paste(val)
        #newImg(temp).save('sample-out'+str(c)+'.png')
        c+=1
        gif['frames'].append(np.asarray(newImg(val)))
    
    gif['len'] = len(gif['frames'])
    

    #gif['frames'][0].save(out, format='GIF', save_all=True, append_images=gif['frames'], duration=gif['delay'], loop=0)
    imageio.mimsave(out, gif['frames'],fps=int(1/(gif['delay']/1000.0)))
else:
    img = pil_image.open(filename)
    newImg(img).save(out)
    
