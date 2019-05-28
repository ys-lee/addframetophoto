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
import numpy as np
import sys
import os
import codecs

def newImg(img, text1, text2):

    new_im = pil_image.open("frame.jpg")
    ratio_w = (img.size[0]*1.0)/885
    ratio_h = (img.size[1]*1.0)/1165

    new_im=new_im.resize((int(new_im.size[0]*ratio_w),int(new_im.size[1]*ratio_h)),1)

    new_im.paste(img, (int(155*ratio_w),
                          int(133*ratio_h)))


    w, h = new_im.size

    font = ImageFont.truetype("PingFang.ttc", int(60*ratio_h))
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
        if text1[i] == u"\n":
            idx+=1
            list_txt.append("")
        elif (draw.textsize(list_txt[idx]+text1[i], font)[0]>1000*ratio_w):
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


def createPhoto(filename, output_filename, message, username):
    if(len(filename.split('.gif'))>1):
        # im is your original image



        img = pil_image.open(filename)
        frames=[]
        frame_infos=[]
        counter = 0

        frame_infos.append(img.tile[0][1])
        #current = img.convert('RGBA').quantize()
        #frames=[current.copy()]
        background = pil_image.new('RGBA', frame_infos[0][2:4], (0, 0, 0,0))

        for jnframes in range(0,img.n_frames):
            nframes=img.n_frames-1-jnframes
            img.seek(nframes)
            info=img.tile[0][1]
            if(jnframes!=img.n_frames-1):
                frame_infos.append(img.tile[0][1])
            p = img.palette.getdata()[1]
            img.putpalette(p)
            background_t=background.copy()
            img_t = pil_image.new('RGBA', (info[2]-info[0],
                                    info[3]-info[1]), (0, 0, 0,0))
            res= pil_image.alpha_composite(img_t, img.convert('RGBA').crop(info))
            background_t.paste(res,info[0:2])
            #background_t.copy().save("test%d.png" % (nframes))
            frames.append(background_t.copy())

        frames2=[]
        for frames in frames[0:len(frames)]:
            frames2.insert(0,frames)

        frames=frames2

        def checkEqual(lst):
            return lst[1:] == lst[:-1]

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
            if(checkEqual(frame_infos)):
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
            #gif['frames'].append(np.asarray(newImg(val)))
            gif['frames'].append(newImg(val, message, username).copy())

        gif['len'] = len(gif['frames'])

        gif['frames'][0].save(output_filename, format='GIF', save_all=True, append_images=gif['frames'][1:], duration=gif['delay'], loop=0)
        #imageio.mimsave(out, gif['frames'],fps=int(1/(gif['delay']/1000.0)))
    else:
        img = pil_image.open(filename)
        newImg(img, message, username).save(output_filename)

DIR_INPUT = "photos"
DIR_OUTPUT = "out3"

# check if output dir exists
if os.path.isdir(DIR_OUTPUT):
    if len(os.listdir(DIR_OUTPUT)) > 0:
        # out dir is not empty
        print 'folder "' + DIR_OUTPUT + '" is not empty, please empty it before generating new photos'
        exit()
else:
    # output dir doesn't exist. mkdir
    os.mkdir(DIR_OUTPUT)

dirs = os.listdir(DIR_INPUT)
for dir in dirs:
    photo_file = ""
    out_file = ""
    message = " "
    user = " "
    for file in os.listdir(os.path.join(DIR_INPUT,dir)):
        if file != "message.txt":
            photo_file = os.path.join(DIR_INPUT,dir,file)
            out_file = os.path.join(DIR_OUTPUT, file)
        else:
            # file = message.txt
            with codecs.open(os.path.join(DIR_INPUT,dir,file), 'r', encoding='utf-8') as fp:
                lines = fp.readlines()
                if len(lines) == 1:
                    message = lines[0]
                elif len(lines) >= 2:
                    message = lines[0]
                    for i in range(1, len(lines)-2+1):
                        message += lines[i]
                    user = lines[len(lines)-1].replace("By ", "")
    createPhoto(photo_file, out_file, message, user)
    for i in range(0,len(message)):
        if (ord(message[i]) >= 0xD800 and ord(message[i]) <= 0xDBFF) or (ord(message[i]) == 0xFE0F):
            print dir
            print message
            print "===="
            break
