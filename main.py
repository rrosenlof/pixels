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
    
  rgb_image.save('swatch.png')
  return rgb_image

def getPaletteOfImg(imgPath):
  img = Image.open(imgPath)

  newPalette = []
  palette = Haishoku.getPalette(imgPath)

  for i in range(0,len(palette)):
    for j in palette[i][1]:
      newPalette.append(j)
  print('   Palette: {}'.format(newPalette))
  return newPalette

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

def pixelate(g, dir, new_dir, contrast_val, color_val, palette=None):

  for filename in os.listdir(dir):
    imgPath = os.path.join(('{}/'.format(dir)),filename)
    img = Image.open(imgPath)
    print('--> {}'.format(imgPath))

    # change contrast and brightness
    contrast = contrast_img(img,contrast_val,color_val)
    # contrast = contrast_img(img)

    # get dims to resize and save contrasted image
    width, height = img.size
    ratio = width/height
    resize_w = g * ratio
    resize_h = g * (1/ratio)
    resize_w = int(round(resize_w,0))
    resize_h = int(round(resize_h,0))
    print('   ratio: {}'.format(ratio))
    print('   orig size: {}, {}'.format(width,height))
    print('   resizes: {}, {}'.format(resize_w, resize_h))

    # resize contrasted image and save it
    contrast = contrast.resize((resize_h,resize_w),resample=Image.BILINEAR)
    contrastFileName = "pxl_{}_{}.png".format(g,os.path.splitext(filename)[0])
    contrastImgPath = os.path.join(('{}/'.format(new_dir)),contrastFileName)
    contrast.save(contrastImgPath, "PNG")
    newContrastImg = Image.open(contrastImgPath)

    # shrink image to create pixels
    imgSmall = contrast.resize((resize_w,resize_h),resample=Image.BILINEAR)
    
    img2 = Image.new('P', (16,16))
    newPalette = []

    # get palette of new image or use the args palette
    if palette is None:
      newPalette = getPaletteOfImg(contrastImgPath)
      img2.putpalette(newPalette * 32)
    else:
      numcolors = len(palette) / 3
      mult = int(256 / numcolors)
      img2.putpalette(palette * mult)

    # change color of the image
    img2 = quantizetopalette(imgSmall,img2,dither=False)
    if img2.mode != 'RGB':
      img2 = img2.convert('RGB')

    # resize the image to original size
    result = img2.resize(img.size,Image.NEAREST)
    
    # save the new image
    newImgFileName = "pxl_{}_{}.png".format(g,os.path.splitext(filename)[0])
    newImgPath = os.path.join(('{}/'.format(new_dir)),newImgFileName)
    print('Saving new image: {}'.format(newImgPath))
    print('type: {}'.format(type(result)))
    result.save(newImgPath, "PNG")

def contrast_img(img, contrast_val=1.0, color_val=1.0):
  # modify the image a bit and return a contrasted copy
  contrast = ImageEnhance.Contrast(img)
  contrast = contrast.enhance(contrast_val)
  contrast = ImageEnhance.Color(contrast)
  contrast = contrast.enhance(color_val)

  return contrast

# Random test array (4):
# ARRAY_COLORS = [0, 0, 4, 127, 149, 127, 40, 187, 40, 33, 33, 240,0,89,166, 0,0,0, 249,243,167]

# Rio Colors Post It collection (5):
# ARRAY_COLORS = [255,153,42,255,104,180,51,153,254,108,219,108,255,212,45]

# Starry Night Colors (8):
ARRAY_COLORS = [0,89,166,51,153,254,83,211,230,0,180,143,255,212,45,249,243,167,0,0,0,255,255,255]

pal = getPaletteOfImg('images/kershisnik.jpg')
makePalette(pal)

# p = makePalette(ARRAY_COLORS)
# pixelate(g=360,dir='images',new_dir='new_images',contrast_val=1.0,color_val=1.0,palette=pal)
pixelate(g=160,dir='single_images',new_dir='new_images',contrast_val=1.0,color_val=1.0,palette=pal) 
