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

def download_sentinel():
    date_img = '2016/5/5'##'2016/9/22' #'2016/6/24'#'2016/5/5'  '2016/12/1' '2016/1/26

    date_img_txt = date_img.replace('/','-')

    #url = 'http://sentinel-s2-l1c.s3.amazonaws.com/tiles/32/U/LV/2016/6/24/0/'
    url = 'http://sentinel-s2-l1c.s3.amazonaws.com/tiles/'
    url2 = 'http://sentinel-s2-l1c.s3-website.eu-central-1.amazonaws.com/#tiles/'
    list_67 = ['32ULV','32UMV','32ULU','32UMU']

    #list_image = ['B01','B02','B03','B04','B05','B06','B07','B08','B8A','B09','B10','B11','B12']
    #list_image = ['B02','B03','B04','B08']
    list_image = ['B11','B8A']
    #list_image = ['B02','B03','B04','B08','B11','B8A']

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

        for img in list_image:
            vrt_list = ''
            vrt_file = output_dir+img+'_'+num+'_'+date_img_txt+'.vrt'
            for cel in list_67:
                dalle = cel[0:2]+'/'+cel[2]+'/'+cel[3:5]+'/'

                """image_data = open_http_query(url+dalle+date_image+'/'+num+'/')
                if not image_data:
                    break
                print image_data.headers"""

                print dalle
                url_image = url+dalle+date_img+'/'+num+'/'+img+'.jp2'
                print url_image
                output_image = output_dir+cel+img+'_'+num+'_'+date_img_txt+'.jp2'
                output_image_tiff = output_dir+cel+img+'_'+num+'_'+date_img_txt+'.tiff'

                file = open_http_query(url_image)
                if file:
                    vrt_list += ' '+output_image_tiff

                    total_size = int(file.headers["Content-Length"])
                    MB_size = total_size/1048576
                    block_size = 1024 * 1024
                    print file.headers["Content-Length"]
                 
                    with open(output_image,'wb') as output:
                        while True:
                            block = file.read(block_size)
                            dSize =  int(os.stat(output_image).st_size)/1048576
                            if not block:
                                break
                            output.write(block)
                    print  "(" + str(dSize) + "/" + str(MB_size) + " MB) " +  url, "Downloaded"
                    win_img = dict_67[cel]
                    print 'gdal_translate -a_nodata 0 -projwin '+win_img['ul_x'] + ' '+win_img['ul_y']+ ' '+win_img['lr_x'] + ' '+win_img['lr_y'] + ' -a_srs EPSG:32632 ' + output_image + ' ' +output_image_tiff

                    sp = subprocess.Popen('gdal_translate -a_nodata 0 -projwin '+win_img['ul_x'] + ' '+win_img['ul_y']+ ' '+win_img['lr_x'] + ' '+win_img['lr_y'] + ' -a_srs EPSG:32632 ' + output_image + ' ' +output_image_tiff)
                    sp.wait()
                    os.remove(output_image)
            sp = subprocess.Popen('gdalbuildvrt -overwrite '+vrt_file+' '+ vrt_list)
            sp.wait() 
            print vrt_list
            
        # composite IR fausses couleur
        sp = subprocess.Popen('gdalbuildvrt -resolution highest -separate '+vrt_ir_false_color+' '+ vrt_list4IR)
        sp.wait() 

        # composite vraies couleur
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

