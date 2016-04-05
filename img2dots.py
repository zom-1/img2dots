#!/usr/bin/env python
# coding: utf-8
import os
import argparse
from PIL import Image  # Pillow or PIL
from PIL import ImageDraw
__author__ = "zom-1"
__version__ = "0.5.1"
__date__ = "2016/04/04"


def img2dots(imgFile, outputFile, mosaicY):
    ''' make a dots picture from image '''
    try:
        img = Image.open(imgFile)
    except IOError:
        print 'cannot open', imgFile
        quit()

    # make mosaic size
    imgSizeX, imgSizeY = img.size
    mosaicX = mosaicY*imgSizeX/imgSizeY
    mosaicSizeX = imgSizeX/mosaicX
    mosaicSizeY = mosaicSizeX

    # make mosaic image
    smlImg = img.resize((mosaicX, mosaicY), Image.ANTIALIAS)  # make a small image
    dotsImg = Image.new("RGB", (mosaicX*mosaicSizeX, mosaicY*mosaicSizeY), "black")  # result
    draw = ImageDraw.Draw(dotsImg)
    for y in range(0, mosaicY):
        for x in range(0, mosaicX):
            r, g, b = smlImg.getpixel((x, y))
            c = "#{0:0>2X}{1:0>2X}{2:0>2X}".format(r, g, b)  # hex, ex)#FF88CC
            draw.ellipse(
                (x*mosaicSizeX+1, y*mosaicSizeY+1, (x+1)*mosaicSizeX-1, (y+1)*mosaicSizeY-1),
                fill=c)
    dotsImg.save(outputFile)

if __name__ == '__main__':
    # args parse
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--vertical_dots", default=30, type=int, help="vertical dots")
    parser.add_argument("-o", "--output_file",  default="",  help="output file")
    parser.add_argument("image_file", help="output a dots image of a given image")
    args = parser.parse_args()
    if (args.output_file):  # if empty, use image basename+'xlsx'
        outputFile = args.output_file
    else:
        outputFile = os.path.splitext(os.path.basename(args.image_file))[0]+"_dots.jpg"

    # exec
    img2dots(args.image_file, outputFile, args.vertical_dots)
