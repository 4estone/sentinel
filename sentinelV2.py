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
    date_img = '2016/5/5'##'2016/9/22' #'2016/6/24'#'2016/5/5'  '2016/12/1' '2016/1/26

    date_img_txt = date_img.replace('/','-')

    list_67 = ['32ULV','32UMV','32ULU','32UMU']

    list_image_init = ['B01_60m','B02_10m','B03_10m','B04_10m','B05_20m','B06_20m','B07_20m','B08_10m','B8A_20m','B09_60m','B11_20m','B12_20m']
    list_image = ['B01','B02','B03','B04','B05','B06','B07','B08','B8A','B09','B11','B12']
    #list_image = ['B02','B03','B04','B08']
    #list_image = ['B01','B05','B06','B07','B8A','B09','B10','B11','B12']


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

    vrt_natural_color = os.path.join(output_dir, lot_date_capture+'_natural.vrt' )
    vrt_ir_false_color = os.path.join(output_dir,  lot_date_capture+'_IR.vrt')
    vrt_list4natural = os.path.join(output_dir,'B04_'+lot_date_capture+'.vrt ')+os.path.join(output_dir, 'B03_'+lot_date_capture+'.vrt ')+ os.path.join(output_dir, 'B02_'+lot_date_capture+'.vrt')
    vrt_list4IR = os.path.join(output_dir,'B08_'+lot_date_capture+'.vrt ')+os.path.join(output_dir, 'B04_'+lot_date_capture+'.vrt ')+os.path.join(output_dir, 'B03_'+lot_date_capture+'.vrt')

    for img in list_image:
        vrt_list = ''
        vrt_file = os.path.join(output_dir, img+'_'+lot_date_capture+'.vrt')
        for tile in list_67:
            #tile_dir = 'S2A_MSIL1C_{}_N0210_R108_T{}_{}'.format(lot_date_capture, tile, lot_date_trans)
            tile_dir = 'S2A_MSIL2A_{}_N0210_R108_T{}_{}'.format(lot_date_capture, tile, lot_date_trans)

            dalle_input = 'T{}_{}_{}.jp2'.format(tile, lot_date_capture, img)
            dalle_out = 'T{}_{}_{}.tiff'.format(tile, lot_date_capture, img)

            full_path = os.path.join(output_dir, tile_dir )

            print dalle_input
            print os.path.join(full_path , dalle_input)
            print os.path.join(full_path, dalle_out)
            #os.rename(os.path.join(full_path , dalle_input), os.path.join(full_path, dalle_out))
            
            input_image = os.path.join(full_path, dalle_input) 
            output_image =  os.path.join(output_dir, dalle_out)

            vrt_list += ' '+output_image
            
            win_img = dict_67[tile]

            print 'gdal_translate -a_nodata 0 -projwin '+win_img['ul_x'] + ' '+win_img['ul_y']+ ' '+win_img['lr_x'] + ' '+win_img['lr_y'] + ' -a_srs EPSG:32632 ' + input_image + ' ' +output_image

            """sp = subprocess.Popen('gdal_translate -a_nodata 0 -co COMPRESS=deflate -projwin '+win_img['ul_x'] + ' '+win_img['ul_y']+ ' '+win_img['lr_x'] + ' '+win_img['lr_y'] + ' -a_srs EPSG:32632 ' + input_image + ' ' +output_image)
            sp.wait()"""
            #os.remove(output_image)"""
        sp = subprocess.Popen('gdalbuildvrt -overwrite '+vrt_file+' '+ vrt_list)
        sp.wait() 

        """sp = subprocess.Popen('gdalinfo -approx_stats '+vrt_file)
        sp.wait() 
        print vrt_list"""
            
    # composite IR fausses couleur
    print 'gdalbuildvrt -resolution highest -separate '+vrt_ir_false_color+' '+ vrt_list4IR
    sp = subprocess.Popen('gdalbuildvrt -resolution highest -separate '+vrt_ir_false_color+' '+ vrt_list4IR)
    sp.wait() 
    """sp = subprocess.Popen('gdalinfo -approx_stats  '+vrt_ir_false_color)
    sp.wait() """
    # composite vraies couleur
    print 'gdalbuildvrt -resolution highest -separate '+vrt_natural_color+' '+ vrt_list4natural
    sp = subprocess.Popen('gdalbuildvrt -resolution highest -separate '+vrt_natural_color+' '+ vrt_list4natural)
    sp.wait() 
    """sp = subprocess.Popen('gdalinfo -approx_stats  '+vrt_natural_color)
    sp.wait()"""

ex = process_sentinel()

