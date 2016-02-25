# -*- coding: utf-8 -*-

import random
import time 
import datetime
import logging

import logging
from oas.oas_api import OASAPI
from oas.ease.api import APIProxy
from oas.ease.exceptions import *
from oas.ease.response import *
from oas.ease.utils import *
from oas.ease.vault import *
from oas.ease.uploader import *
from oas.ease.job import *

import os

logging.basicConfig(filename = 'test_yq.log',level = logging.DEBUG,filemode = 'a', format = '%(asctime)s -%(name)s %(lineno)d %(funcName)s: %(message)s')
# LOG_FILE="test_yq.log"
# handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes = 1024*1024, backupCount = 5)
# fmt = '%(asctime)s - %(filename)s:%(lineno)s - %(name)s - %(message)s'  
# formatter = logging.Formatter(fmt)
# handler.setFormatter(formatter)
# log.addHandler(handler)
# log.setLevel(logging.DEBUG)

api = OASAPI('cn-hangzhou.oas.aliyuncs.com', 'eygUsBeE9HAp0ltu', 'v5oQ7ZmxaDpSaWLzfHJLermnGSFpDI')
vault = Vault.create_vault(api, 'szyq')

path='d:/HD_YQ_interface/Data/Export/'

archive_id_list=[]

today = datetime.datetime.now()
t = datetime.datetime.now().strftime("%Y%m%d")
yesterday = today - datetime.timedelta(days=1)
y=yesterday.strftime("%Y%m%d")

t_file=['Goods/goods_'+t+'.csv','Ordertl/Ordertl_'+t+'.csv','RPT_STORESALEDRPT/RPT_STORESALEDRPT_'+t+'.csv','RPT_STORESALEDRPT/v_cl_actinvs_'+t+'.csv','RPT_STORESALEMRPT/MRPT_STORESALEDRPT_'+t+'.csv','store/cl_gdstore_'+t+'.csv','store/storerefinfo_'+t+'.csv']
y_file=['Goods/goods_'+y+'.csv','Ordertl/Ordertl_'+y+'.csv','RPT_STORESALEDRPT/RPT_STORESALEDRPT_'+y+'.csv','RPT_STORESALEDRPT/v_cl_actinvs_'+y+'.csv','RPT_STORESALEMRPT/MRPT_STORESALEDRPT_'+y+'.csv','store/cl_gdstore_'+y+'.csv','store/storerefinfo_'+y+'.csv']



def get_archive_id(archive_id):
    archive_id_list.append(archive_id)
    return archive_id_list


def upload():
    for name in t_file:
        fname = name.split('/')
        truenama = fname[1]
        todayfile = path + name

        if os.path.exists(todayfile):
            print 'start upload '+fname[1]
            logging.info(fname[1]+":start")
            archive_id = vault.upload_archive(todayfile)
            #f = open('e:/banben/upload/archive_id.txt','a')
            #f.write(archive_id+'\n')
            get_archive_id(archive_id)
            print archive_id
            logging.info('get:'+archive_id)

        else:
            print 'no such file:',todayfile
            logging.info(todayfile+' is not find!')
    #f.close()
    clearfile()
    print 'uploading done!'
    logging.info('uploading done!')
    #print archive_id_list

def clearfile():
    for name in y_file:
        yesterdayfile = path + name
        if os.path.exists(yesterdayfile):
            os.remove(yesterdayfile)
        else:
            pass


def set_archive_id():
    pass

# def delete():
#     archive_id = upload()
#     vault.delete_archive(archive_id)
#     print archive_id,'has deleted!'

# def download():
    #archive_id = upload()
    # archive_id_list = get_archive_id(archive_id)
    # for archive_id in archive_id_list:
    #     print 'archive_id:',archive_id
    # archive_id='49B0489E15A390802E0E369E2DD4384A0D40B15A6F654D3D9355C4C81182FFBBD3C5A7CC08BE132F91DA8E7CF53DFA98F17A6D64BD6D0C2CB546832574CAB70C'
    # job = vault.retrieve_archive(archive_id)
    # job.download_to_file(localpath)

if __name__ == '__main__':
    #upload()
    download()

