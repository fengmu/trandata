# -*- coding: utf-8 -*-

import sys
import logging
import requests

from upload.oss_upload import upload

logging.basicConfig(filename = 'szyq.log',level = logging.DEBUG,filemode = 'a', format = '%(asctime)s -%(name)s %(lineno)d %(funcName)s: %(message)s')


def execupload():
    upload()


tasks={
    "upload":{"cmdcode":"upload",
                "cmdcontent":"e:/yzapp/yztran/scripts/python e:/yzapp/yztran/prj/app/crontask.py upload 0",
                "second":"0",
                "minute":"29",
                "hour":"15",
                "tasktag":"1"
                },

    }



def exec_0(funcname):
    print 'exec'+funcname
    logging.info(funcname+":start")
    exec 'exec'+funcname+'()'
    logging.info(funcname+":end")
    
def exec_1(funcname):    
    try:
        argv = tasks[funcname]
        url = "http://127.0.0.1:20666/setjob"      
        r = requests.post(url, data=argv)
        print r.text
    except:
        argv = tasks[funcname]
        url = "http://127.0.0.1:20666/setjob"      
        r = requests.post(url, data=argv)
        print r.text
        print "error"
    
    
if __name__ == '__main__':
    print sys.argv[0]
    arg1 = sys.argv[1]
    arg2 = sys.argv[2]  #0 立即执行, 1。注册到任务服务器
    if len(arg1) == 0 or len(arg2) == 0:
        print "请输入参数"
    else:   
        if arg2 == "0":
            exec_0(arg1)
        else:
            exec_1(arg1)
