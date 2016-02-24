# -*- coding: utf-8 -*-

import random
import time 
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

path='e:/banben/upload/upload/'

archive_id_list=[]
filename=['a.txt','b.txt','c.txt','d.txt']

#localpath="e:/banben/upload/2.xlsx"

def get_archive_id(archive_id):
    archive_id_list.append(archive_id)
    return archive_id_list


def upload():
    for name in filename:
        print 'start upload '+name
        logging.info(name+":start")
        archive_id = vault.upload_archive(path+name)
        get_archive_id(archive_id)
        print archive_id
        logging.info('get:'+archive_id)
    print 'uploading success!'
    logging.info('uploading success!')


# def delete():
#     archive_id = upload()
#     vault.delete_archive(archive_id)
#     print archive_id,'has deleted!'

# def download():
#     archive_id = upload()
#     job = vault.retrieve_archive(archive_id)
#     job.download_to_file(localpath)

if __name__ == '__main__':
    upload()

