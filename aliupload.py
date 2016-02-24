# -*- coding: utf-8 -*-

import random
import time 
import logging

import logging.handlers  
from oas.oas_api import OASAPI
from oas.ease.api import APIProxy
from oas.ease.exceptions import *
from oas.ease.response import *
from oas.ease.utils import *
from oas.ease.vault import *
from oas.ease.uploader import *
from oas.ease.job import *

import os

LOG_FILE="test.log"
handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes = 1024*1024, backupCount = 5)
fmt = '%(asctime)s - %(filename)s:%(lineno)s - %(name)s - %(message)s'  
formatter = logging.Formatter(fmt)
handler.setFormatter(formatter)
log.addHandler(handler)
log.setLevel(logging.DEBUG)


class TestConf(object):

    def __init__(self):
        self.host = 'cn-hangzhou.oas.aliyuncs.com'
        self.accesskey_id = "eygUsBeE9HAp0ltu"
        self.accesskey_secret = "v5oQ7ZmxaDpSaWLzfHJLermnGSFpDI"
        self.vault_name = "szyq"
        # self.vault_name_test = "test"

        # self.osshost = "您要转储的oss域名"
        # self.bucket = "您要转储的bucket"
        # self.object = "您要转储的Object"

conf = TestConf()


class TestDemo():
    _MEGABYTE = 1024 * 1024


    def __init__(self):
        self.api = OASAPI(conf.host, conf.accesskey_id, conf.accesskey_secret)
        self.api_proxy = APIProxy(self.api)
        self.vault_name = conf.vault_name
        # self.vault_name_test = conf.vault_name_test

        self.file_big = "random100M.bin"
        self.file_big_size = 200*self._MEGABYTE

        with open(self.file_big, 'wb+') as f:
            self.write_random_data(f, self.file_big_size)

        self.file_small = "random30M.bin"
        self.file_small_size = 30*self._MEGABYTE

        with open(self.file_small, 'wb+') as f:
            self.write_random_data(f, self.file_small_size)


    def write_random_data(self, file, size):
        remaining = size
        while remaining > 0:
            n = min(remaining, 1024)
            random_data = os.urandom(n)
            file.write(random_data)
            remaining = remaining - n

            n = min(remaining, 1024 * random.randint(256, 1024))
            file.write('\0' * n)
            remaining = remaining - n


    def test_single_archive_upload(self):
        print '''
########################################################
 Using the low level api method to upload a small archive 
#########################################################'''
        res = self.api_proxy.create_vault(self.vault_name)
        vault_id = res['x-oas-vault-id']

        etag = compute_etag_from_file(self.file_small)
        tree_etag = compute_tree_etag_from_file(self.file_small)
        with open(self.file_small, 'rb') as f:
            content = f.read()
            res = self.api_proxy.post_archive(vault_id, content, etag, tree_etag)
            archive_id = res['x-oas-archive-id']
        print "archive_id",archive_id

    #test the multipart upload by the proxy api, and this is low level api
    def test_multi_upload(self):
        print '''\n\n\n
########################################################
 Using the low level api to invoke the multipart api and implement the archive uplod
#########################################################'''
        res = self.api_proxy.create_vault(self.vault_name)
        vault_id = res['x-oas-vault-id']

        part_size = 1024 * 1024 * 64


        etag_array= []
        tree_etag_array= []
        offset = 0

        cur_part_num=0
        cur_start_pos = 0
        cur_end_pos = 0
        print "1. comput the etag,tree-etag"
        print "1.1 comput the  etag , tree_etag of part" 
        while True:
            tmpsize = part_size
            if(cur_start_pos + tmpsize > self.file_big_size):
                tmpsize = self.file_big_size - cur_start_pos;
            cur_end_pos += tmpsize -1

            etag_array.append(compute_etag_from_file(self.file_big, cur_start_pos, tmpsize) )
            tree_etag_array.append(compute_tree_etag_from_file(self.file_big, cur_start_pos, tmpsize))

            cur_start_pos += tmpsize
            cur_part_num += 1
            if(cur_start_pos >= self.file_big_size-1):
                break;

        print "1.2 comput the  total tree_etag of the archive" 
        tree_etag_total = compute_combine_tree_etag_from_list( tree_etag_array) ;

        print "2.1 init the upload task, and get the uploadId"
        res = self.api_proxy.create_multipart_upload(vault_id, part_size)
        upload_id = res['x-oas-multipart-upload-id']
        print "upload_id",upload_id

        f = open(self.file_big, 'rb')

        cur_part_num = 0
        cur_start_pos = 0
        cur_end_pos = 0
        while True:
            tmpsize = part_size
            if(cur_start_pos + tmpsize > self.file_big_size):
                tmpsize = self.file_big_size - cur_start_pos;

            cur_end_pos += tmpsize
            print "2.2 upload every part to oas server, and the etag of the part will be used. current part is:", cur_part_num+1
            self.api_proxy.post_multipart_from_reader(vault_id, upload_id, f, tmpsize,('%d-%d' %(cur_start_pos, cur_end_pos-1)), etag_array[cur_part_num],tree_etag_array[cur_part_num])

            cur_start_pos += tmpsize
            cur_part_num += 1
            if(cur_end_pos>= self.file_big_size -1):
                break;

        print "2.3 complete the multipart task, and the total etag will be used"
        res = self.api_proxy.complete_multipart_upload(
                        vault_id, upload_id, self.file_big_size, tree_etag_total)
        print "output the archive id"
        archive_id = res['x-oas-archive-id']
        print "archive_id",archive_id
        return archive_id

    #test the uploader to upload big file, and this is high level api
    def test_uploader(self):
        print '''\n\n\n
########################################################
 Using the High level api to invoke the multipart api 
#########################################################'''
        vault = Vault.create_vault(self.api, self.vault_name)

        print "initial a uploadId"
        uploader = vault.initiate_uploader(self.file_big)
        uploader_id = uploader.id
        print "uploader_id",uploader_id

        print "start the multipart" 
        archive_id = uploader.start()

        print "finish the upload, and output the archive_id"
        print "archive_id",archive_id
        return archive_id


    #to inquire the archive list of vault
    def test_vault_retrieve(self):
        print '''\n\n\n
########################################################
 Retrieve the vault info, and inquire the archive list of the vault 
#########################################################'''
        vault = Vault.create_vault(self.api, self.vault_name)
        job = vault.retrieve_inventory()
        job.download_to_file(job.id)

    #to test download archive
    def test_download_archive(self, archive_id):
        print '''\n\n\n
########################################################
 Submit the archive job and download the job to local 
#########################################################'''
        vault = Vault.create_vault(self.api, self.vault_name)
        job = vault.retrieve_archive(archive_id)
        job.update_status()
        if not job.completed:
            job.download_to_file(file_path = job.id, block = True)

    #test delete archive
    def test_delete_archive(self, archive_id):
        print '''\n\n\n
########################################################
 Delete the archive 
#########################################################'''
        vault = Vault.create_vault(self.api, self.vault_name)
        vault.delete_archive(archive_id)

#     def test_pull_from_oss(self):
#         print '''\n\n\n
# ########################################################
#  submit a pull-from-oss job and OAS will finish the pull of OSS object to OAS 
# #########################################################'''
#         vault = Vault.create_vault(self.api, self.vault_name)
#         # create vault
#         job = vault.pull_from_oss(conf.osshost, conf.bucket, conf.object, "test desc")
#         job._check_status(block=True)

#         # delete archive
#         print "bucket:%s object:%s finish pull from oss,\n archiveId:%s" % (conf.bucket, conf.object, job.archive_id)


#     def test_push_to_oss(self):
#         print '''\n\n\n
# ########################################################
#  submit a push-to-oss job and OAS will finish the push of OAS archive to OSS 
# #########################################################'''
#         vault = Vault.create_vault(self.api, self.vault_name)
#         archive_id = vault.upload_archive(self.file_big)
#         job = vault.push_to_oss(archive_id, conf.osshost, conf.bucket, archive_id, "test desc")
#         job._check_status(block=True)
#         print archive_id + " finish push to oss"        

if __name__ == '__main__':
    t = TestDemo()

    t.test_single_archive_upload()
    t.test_multi_upload();

    archive_id = t.test_uploader();

    t.test_vault_retrieve();
    t.test_download_archive(archive_id)
    t.test_delete_archive(archive_id)

    # t.test_pull_from_oss()
    # t.test_push_to_oss()