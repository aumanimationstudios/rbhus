#!/usr/bin/env python3
#-*- coding: utf-8 -*-
__author__ = "Shrinidhi Rao"
__license__ = "GPL"
__email__ = "shrinidhi666@gmail.com"



import zipfile
import os
# import PIL
from lxml import etree as ET
import sys
import subprocess

__author__ = 'pierre'

ns = {'kra': 'http://www.calligra.org/DTD/krita'}


class Kra(object):
    maindoc_xml = None
    merged_image = None
    basename = None
    icc = None
    icc_path = None
    kra_name = None

    def __init__(self, krafile):
        kra = zipfile.ZipFile(krafile)

        self.__merged_image_path = None

        self.filename = os.path.basename(krafile)

        self.basename, _ = self.filename.split('.')

        self.merged_image = kra.read('mergedimage.png')

        self.xml = ET.fromstring(kra.read('maindoc.xml'))
        self.kra_name = self.xml.find('.//kra:IMAGE', ns).attrib['name']

        self.icc = kra.read('{basename}/annotations/icc'.format(basename=self.kra_name))

    @property
    def merged_image_path(self):
        return self.__merged_image_path

    @merged_image_path.setter
    def merged_image_path(self, path):
        self.__merged_image_path = path

    def get_basename(self):
        return self.basename

    def get_merged_image(self):
        return self.merged_image

    def get_icc(self):
        x = self.xml.find('.//kra:IMAGE', ns)
        icc_name = x.attrib['profile']
        return {'name': icc_name, 'data': self.icc}



if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python3 krita-thumbnailer.py <input.kra> <output.png>")
        sys.exit(1)

    input_file = os.path.abspath(sys.argv[1])
    output_file = os.path.abspath(sys.argv[2])

    # Process the .kra file
    krafile = Kra(input_file)
    png_data = krafile.get_merged_image()

    # Write the PNG data to the specified output file
    with open(output_file, 'wb') as f:
        f.write(png_data)

    # Use ImageMagick to resize the image to 96x96
    resized_output_file = output_file  # Overwrite the same output file
    subprocess.run(
        ["/usr/bin/magick", output_file, "-sample", "96x96", resized_output_file],
        check=True
    )

    print(f"Thumbnail saved and resized to {resized_output_file}")

