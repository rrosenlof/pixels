from haishoku.haishoku import Haishoku
from PIL import Image
import pprint

img_path = 'images/kershisnik.jpg'
haishoku = Haishoku.loadHaishoku(img_path)

Haishoku.showPalette(img_path)
palette = Haishoku.getPalette(img_path)
print('palette: {}'.format(palette))

