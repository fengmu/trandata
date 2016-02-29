# -*- coding: utf-8 -*-

from __future__ import print_function

import time 
import datetime
import logging

import os, sys
import oss2

logging.basicConfig(filename = 'szyq.log',level = logging.DEBUG,filemode = 'a', format = '%(asctime)s -%(name)s %(lineno)d %(funcName)s: %(message)s')

today = datetime.datetime.now()
t = datetime.datetime.now().strftime("%Y%m%d")
yesterday = today - datetime.timedelta(days=1)
y=yesterday.strftime("%Y%m%d")

path='d:/HD_YQ_interface/Data/Export/'
t_file=['Goods/goods_'+t+'.csv','Orderdtl/Orderdtl_'+t+'.csv','RPT_STORESALEDRPT/RPT_STORESALEDRPT_'+t+'.csv','RPT_STORESALEDRPT/v_cl_actinvs_'+t+'.csv','RPT_STORESALEMRPT/MRPT_STORESALEDRPT_'+t+'.csv','store/cl_gdstore_'+t+'.csv','store/storerefinfo_'+t+'.csv']
#t_file=['1.txt','2.txt','3.txt']
y_file=['Goods/goods_'+y+'.csv','Ordertl/Ordertl_'+y+'.csv','RPT_STORESALEDRPT/RPT_STORESALEDRPT_'+y+'.csv','RPT_STORESALEDRPT/v_cl_actinvs_'+y+'.csv','RPT_STORESALEMRPT/MRPT_STORESALEDRPT_'+y+'.csv','store/cl_gdstore_'+y+'.csv','store/storerefinfo_'+y+'.csv']

auth = oss2.Auth('YrQYqTR97x9brbzm','FkDpAXR5tBYlRaNanhBMYenzAY0FJh')
service = oss2.Service(auth,'oss-cn-hangzhou.aliyuncs.com')

#print([b.name for b in oss2.BucketIterator(service)])

bucket = oss2.Bucket(auth, 'http://oss-cn-hangzhou.aliyuncs.com', 'szyq')


def percentage(consumed_bytes, total_bytes):
    if total_bytes:
        rate = int(100 * (float(consumed_bytes) / float(total_bytes)))
        print('\r{0}% '.format(rate), end='')

        sys.stdout.flush()

#上传
#bucket.put_object_from_file('upload.zip', 'e:/GS/SZ_youqi/upload.zip')
def upload():
    for name in t_file:
        fname = name.split('/')
        truename = fname[1]
        todayfile = path + name

        if os.path.exists(todayfile):
            print('\n'+'start upload '+truename)
            logging.info(truename+":start")
            #bucket.put_object_from_file(name, todayfile ,progress_callback=percentage)
            bucket.put_object_from_file(truename, todayfile ,progress_callback=percentage)
            logging.info(truename+":finish")

        else:
			#pass
            print('no such file:'+truename)
            logging.info(truename+' is not find!')

    print('uploading done!')
    logging.info('uploading done!')

def clearfile():
    for name in y_file:
        yesterdayfile = path + name
        if os.path.exists(yesterdayfile):
            os.remove(yesterdayfile)
            logging.info(name+" delete!")
        else:
            pass

#下载
#bucket.get_object_to_file('a.txt', 'e:/banben/upload/upload.zip')


if __name__ == '__main__':
    upload()