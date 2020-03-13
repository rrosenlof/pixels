#!/usr/local/bin/python3
from PIL import Image
import os
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
  print('pal: {}'.format(pal))
  counter = 1
  for filename in os.listdir('images'):
    imgPath = os.path.join('images/',filename)
    img = Image.open(imgPath)



    imgSmall = img.resize((16,16),resample=Image.BILINEAR)

    img2 = Image.new('P', (16,16))
    img2.putpalette(pal * 51)
    img2 = quantizetopalette(imgSmall,img2,dither=False)
    # img2.show()
    if img2.mode != 'RGB':
      img2 = img2.convert('RGB')

    result = img2.resize(img.size,Image.NEAREST)

    newImgFileName = "new_{}.jpeg".format(counter)
    counter += 1
    newImgPath = os.path.join('new_images/',newImgFileName)
    print('Saving new image: {}'.format(newImgPath))
    result.save(newImgPath)


# ARRAY_COLORS = [0, 0, 4, 127, 149, 127, 40, 187, 40, 33, 33, 240]
ARRAY_COLORS = [255,153,42,255,104,180,51,153,254,108,219,108,255,212,45]

# p = makePalette(ARRAY_COLORS)
pixelate(pal=ARRAY_COLORS) 