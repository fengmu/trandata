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

api = OASAPI('cn-hangzhou.oas-internal.aliyuncs.com', 'eygUsBeE9HAp0ltu', 'v5oQ7ZmxaDpSaWLzfHJLermnGSFpDI')
vault = Vault.create_vault(api, 'szyq')

t = datetime.datetime.now().strftime("%Y%m%d")

path = 'd:/HD_YQ_interface/Data/Export/'
dfile = ['Goods/goods_'+t+'.csv','Ordertl/Ordertl_'+t+'.csv','RPT_STORESALEDRPT/RPT_STORESALEDRPT_'+t+'.csv','RPT_STORESALEDRPT/v_cl_actinvs_'+t+'.csv','RPT_STORESALEMRPT/MRPT_STORESALEDRPT_'+t+'.csv','store/cl_gdstore_'+t+'.csv','store/storerefinfo_'+t+'.csv']


def get_archive_id():
    pass

def download():
    #get_archive_id()   
    for name in dfile:
        localpath = path + name
        job = vault.retrieve_archive(archive_id)
        job.download_to_file(localpath)

if __name__ == '__main__':
    download()