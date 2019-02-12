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

def download_sentinel():
    date_img = '2016/6/24'
    #date_img = '2016/9/22'

    date_img_txt = date_img.replace('/','-')

    #url_format = 'http://sentinel-s2-l1c.s3.amazonaws.com/tiles/32/U/LV/2016/6/24/0/'
    url = 'http://sentinel-s2-l1c.s3.amazonaws.com/tiles/'
    url2 = 'http://sentinel-s2-l1c.s3-website.eu-central-1.amazonaws.com/#tiles/'
    list_67 = ['32ULV','32UMV','32ULU','32UMU']

    #list_image = ['B01','B02','B03','B04','B05','B06','B07','B08','B8A','B09','B10','B11','B12']
    list_image = ['B02','B03','B04','B08']
    list_file = ['metadata.xml','productinfo.json']
    win_32ULV =  {'ul_x':'342000', 'ul_y':'5445000', 'lr_x':'400000', 'lr_y':'5400000'}
    win_32UMV = {'ul_x':'400000', 'ul_y':'5445000', 'lr_x':'450000', 'lr_y':'5400000'}
    win_32ULU =  {'ul_x':'342000', 'ul_y':'5400000', 'lr_x':'400000', 'lr_y':'5320000'}
    win_32UMU = {'ul_x':'400000' ,'ul_y':'5400000' ,'lr_x':'450000' ,'lr_y':'5320000'}

    dict_67 = {'32ULV':win_32ULV,'32UMV':win_32UMV, '32ULU':win_32ULU, '32UMU':win_32UMU}

    output_dir = 'C:/Temp/'

    for num in ('0','1'):
        vrt_natural_color = output_dir+num+'_'+date_img_txt+'_natural.vrt'
        vrt_ir_false_color = output_dir+num+'_'+date_img_txt+'_IR.vrt'
        vrt_list4natural = output_dir+'B04_'+num+'_'+date_img_txt+'.vrt '+output_dir+'B03_'+num+'_'+date_img_txt+'.vrt '+output_dir+'B02_'+num+'_'+date_img_txt+'.vrt'
        vrt_list4IR = output_dir+'B08_'+num+'_'+date_img_txt+'.vrt '+output_dir+'B04_'+num+'_'+date_img_txt+'.vrt '+output_dir+'B03_'+num+'_'+date_img_txt+'.vrt'

            
        # composite IR fausses couleur
        sp = subprocess.Popen('gdalbuildvrt -resolution highest -separate '+vrt_ir_false_color+' '+ vrt_list4IR)
        sp.wait() 

        # composite vraies couleur
        print 'gdalbuildvrt -resolution highest -separate '+vrt_natural_color+' '+ vrt_list4natural

        sp = subprocess.Popen('gdalbuildvrt -resolution highest -separate '+vrt_natural_color+' '+ vrt_list4natural)
        sp.wait() 

def open_http_query(url):
    try:
        request = Request(url)
        response = urlopen(request, timeout=30)
        return response
    except URLError:
        return None

ex = download_sentinel()

