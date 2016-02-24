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

LOG_FILE="test_yq.log"
handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes = 1024*1024, backupCount = 5)
fmt = '%(asctime)s - %(filename)s:%(lineno)s - %(name)s - %(message)s'  
formatter = logging.Formatter(fmt)
handler.setFormatter(formatter)
log.addHandler(handler)
log.setLevel(logging.DEBUG)

api = OASAPI('cn-hangzhou.oas.aliyuncs.com', 'eygUsBeE9HAp0ltu', 'v5oQ7ZmxaDpSaWLzfHJLermnGSFpDI')

vault = Vault.create_vault(api, 'szyq')

path='e:/banben/upload/1.xlsx'

def upload():
    archive_id = vault.upload_archive(path)
    return archive_id


def delete():
    archive_id = upload()
    vault.delete_archive(archive_id)
    print archive_id,'has deleted!'

def download():
    archive_id = upload(path)
    job = vault.retrieve_archive(archive_id)
    job.download_to_file(localpath)

if __name__ == '__main__':
    upload()

