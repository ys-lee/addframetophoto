#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 23 17:33:33 2018

@author: gregory
"""

from PIL import Image


def iter_frames(im):
    try:
        i= 0
        while 1:
            im.seek(i)
            imframe = im.copy()
            if i == 0: 
                palette = imframe.getpalette()
            else:
                imframe.putpalette(palette)
            yield imframe
            i += 1
    except EOFError:
        pass

im=Image.open("pp.gif")
for i, frame in enumerate(iter_frames(im)):
    frame.save('test%d.png' % i,**frame.info)