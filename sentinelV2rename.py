# -*- coding: utf-8; -*-

from urllib2 import Request, urlopen, URLError
import os
import subprocess
import io
from uuid import uuid4

try:
	from osgeo import gdal
	from osgeo.gdalconst import *
	from osgeo import ogr
	from osgeo import osr
except Exception, err:
	cfg.testGDALV = err

def process_sentinel():
    list_67 = ['32ULV','32UMV','32ULU','32UMU']
    list_image_init = ['B01_60m','B02_10m','B03_10m','B04_10m','B05_20m','B06_20m','B07_20m','B08_10m','B8A_20m','B09_60m','B11_20m','B12_20m']
    list_image = ['B01','B02','B03','B04','B05','B06','B07','B08','B8A','B09','B11','B12']


    list_file = ['metadata.xml','productinfo.json']
    win_32ULV =  {'ul_x':'342000', 'ul_y':'5445000', 'lr_x':'400000', 'lr_y':'5400000'}
    win_32UMV = {'ul_x':'400000', 'ul_y':'5445000', 'lr_x':'450000', 'lr_y':'5400000'}
    win_32ULU =  {'ul_x':'342000', 'ul_y':'5400000', 'lr_x':'400000', 'lr_y':'5320000'}
    win_32UMU = {'ul_x':'400000' ,'ul_y':'5400000' ,'lr_x':'450000' ,'lr_y':'5320000'}

    dict_67 = {'32ULV':win_32ULV,'32UMV':win_32UMV, '32ULU':win_32ULU, '32UMU':win_32UMU}

    output_dir = 'C:\Temp\sentinel'

    #dir_prefix = 'S2A_MSIL1C_20180912T103021_N0206_R108_T'
    tmp = 'S2A_MSIL2A_20181111T103241_N0210_R108_T32ULU_20181111T120713'
    dir_prefix = 'S2A_MSIL2A_20181111T103241_N0210_R108_T'
    lot_date_capture = '20181111T103241'
    lot_date_trans = '20181111T120713'

    for img in list_image_init:
        imgIndex = list_image_init.index(img)
        imgOut = list_image[imgIndex]
        for tile in list_67:
            #tile_dir = 'S2A_MSIL1C_{}_N0210_R108_T{}_{}'.format(lot_date_capture, tile, lot_date_trans)
            tile_dir = 'S2A_MSIL2A_{}_N0210_R108_T{}_{}'.format(lot_date_capture, tile, lot_date_trans)

            full_path = os.path.join(output_dir, tile_dir )
            dalle_input = 'T{}_{}_{}.jp2'.format(tile, lot_date_capture, img)
            dalle_out = 'T{}_{}_{}.jp2'.format(tile, lot_date_capture, imgOut)
            print os.path.join(full_path , dalle_input)
            print os.path.join(full_path, dalle_out)
            os.rename(os.path.join(full_path , dalle_input), os.path.join(full_path, dalle_out))




ex = process_sentinel()

