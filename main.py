#!/usr/local/bin/python3
from PIL import Image, ImageEnhance
import os
import operator
from collections import defaultdict
import re
import functools
from haishoku.haishoku import Haishoku

def makePalette(array_colors):
  # Also the number of colors:
  THUMBNAILS_PER_ROW = 6
  THUMBNAIL_WIDTH = 10
  THUMBNAIL_HEIGHT = 10
  MODE = 'RGB'
  
  width = THUMBNAILS_PER_ROW * THUMBNAIL_WIDTH
  height = THUMBNAIL_HEIGHT
  rgb_image = Image.new(MODE, (width,height),color=0)
  color_c = 0
  for i in range(0,THUMBNAILS_PER_ROW):
    im = Image.new(MODE, (THUMBNAIL_WIDTH,THUMBNAIL_HEIGHT),color=(array_colors[color_c],array_colors[color_c+1],array_colors[color_c+2]))
    color_c += 3
    rgb_image.paste(im,((i)*THUMBNAIL_WIDTH,0), mask=None)
    
  rgb_image.save('swatch.jpeg')
  return rgb_image

def quantizetopalette(silf, palette, dither=False):
    """Convert an RGB or L mode image to use a given P image's palette."""

    silf.load()

    # use palette from reference image
    palette.load()
    if palette.mode != "P":
        raise ValueError("bad mode for palette image")
    if silf.mode != "RGB" and silf.mode != "L":
        raise ValueError(
            "only RGB or L mode images can be quantized to a palette"
            )
    im = silf.im.convert("P", 1 if dither else 0, palette.im)
    # the 0 above means turn OFF dithering

    # Later versions of Pillow (4.x) rename _makeself to _new
    try:
        return silf._new(im)
    except AttributeError:
        return silf._makeself(im)

def pixelate(pal):
  for filename in os.listdir('images'):
    imgPath = os.path.join('images/',filename)
    img = Image.open(imgPath)

    # modify the image a bit and save a contrasted copy
    contrast = ImageEnhance.Contrast(img)
    contrast = contrast.enhance(1.4)
    contrast = ImageEnhance.Color(contrast)
    contrast = contrast.enhance(2.5)
    contrast = contrast.resize((256,256),resample=Image.BILINEAR)
    contrastFileName = "contrast_{}".format(filename)
    contrastImgPath = os.path.join('contrast_images/',contrastFileName)
    contrast.save(contrastImgPath, "PNG")
    newContrastImg = Image.open(contrastImgPath)

    # get palette
    palette = Haishoku.getPalette(contrastImgPath)
    print('palette: {}'.format(palette))

    # change format of palette to remove percents
    newPalette = []
    for i in range(0,8):
      for j in palette[i][1]:
        newPalette.append(j)
    print(newPalette)

    # shrink image to create pixels
    imgSmall = contrast.resize((172,172),resample=Image.BILINEAR)

    # change color of the image
    img2 = Image.new('P', (16,16))
    img2.putpalette(newPalette * 32)
    img2 = quantizetopalette(imgSmall,img2,dither=False)
    if img2.mode != 'RGB':
      img2 = img2.convert('RGB')

    # resize the image to original size
    result = img2.resize(img.size,Image.NEAREST)

    # save the new image
    newImgFileName = "new_{}".format(filename)
    newImgPath = os.path.join('new_images/',newImgFileName)
    print('Saving new image: {}'.format(newImgPath))
    result.save(newImgPath, "PNG")

# Random test array (4):
# ARRAY_COLORS = [0, 0, 4, 127, 149, 127, 40, 187, 40, 33, 33, 240]

# Rio Colors Post It collection (5):
#ARRAY_COLORS = [255,153,42,255,104,180,51,153,254,108,219,108,255,212,45]

# Starry Night Colors (8):
ARRAY_COLORS = [0,89,166,51,153,254,83,211,230,0,180,143,255,212,45,249,243,167,0,0,0,255,255,255]


# p = makePalette(ARRAY_COLORS)
pixelate(pal=ARRAY_COLORS) 
