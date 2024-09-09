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


if (__name__ == '__main__'):
    krafile = Kra(os.path.abspath(sys.argv[1]))
    pngfile = os.path.abspath(sys.argv[2])
    png = krafile.get_merged_image()
    with open(pngfile, 'wb') as f:
        f.write(png)
        f.close()
