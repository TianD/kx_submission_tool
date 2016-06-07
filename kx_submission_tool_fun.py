#coding:utf-8
'''
Created on 2016年6月6日 下午3:23:01

@author: TianD

@E-mail: tiandao_dunjian@sina.cn

@Q    Q: 298081132

@Description: define functions

'''

import os, os.path
from PyQt4 import QtCore
from kx_submission_tool_sequenceFileDetection import SequenceFileDetection
from kx_submission_tool_projectMatch import ProjNameMatch

def parseCmd(path, mod = 1):
    result = []
    option = QtCore.QVariant("Normal")
    for root, dirs, files in os.walk(path):
        """将序列文件转换成项目需要的ffmpeg格式"""
        sfd = SequenceFileDetection()
        sfd.setSequenceFiles(files)
        dic = sfd.getSequenceInfo(mod)
        if 'stereoCameraLeft' in root or 'CamL' in root:
            option = QtCore.QVariant("Left")
        elif 'stereoCameraRight' in root or 'CamR' in root:
            option = QtCore.QVariant("Right")
        else :
            pass
        for key, value in dic.iteritems():
            if key == "separateFiles":
                pnm = ProjNameMatch()
                for v in value:
                    pnm.setFileName(v)
                    if pnm.matchProjName():
                        result.append(['b', os.path.join(root, v), '', option, 0])
            else :
                framePrefix = key.split('.')[-2].split('%')[0]
                frameStart = value[0]
                frameEnd = value[1]
                frameMiss = value[-1]
                if frameMiss :
                    miss = '-'.join([','.join(['{0}'.format(f-1), '{0}'.format(f+1)]) for f in frameMiss])
                    frameRange = "{0}{1}-{3}-{0}{2}".format(framePrefix, frameStart, frameEnd, miss)
                else :
                    frameRange = "{0}{1}-{0}{2}".format(framePrefix, frameStart, frameEnd)
                result.append(['a', os.path.join(root, key), frameRange, option, 0])
            
    return result


def copyCmd(data):
    fileName = os.path.basename(data[1])
    pnm = ProjNameMatch()
    pnm.setFileName(fileName)
    pnm.setPrefix(mod=1)
    uploadPath = pnm.getUploadServerPath(mod='Images')
    print uploadPath
    
def getFrames(frameRange):
    sections = frameRange.split(",")
    frameLst = []
    for section in sections:
        startEnd = section.split("-")
        if len(startEnd) == 1:
            start = startEnd[0]
            end = startEnd[0]
        else :
            start, end = startEnd
        thisRange = range(int(start), int(end)+1)
        frameLst.extend(thisRange)
    return frameLst
        
if __name__ == "__main__":
    '''
    [
    ['a','ROCK_001_001_001_an_c001', '1001-1100', QtCore.QVariant('Left'), 0],
    ['b','ROCK_002_002_002_an_c001', '1001-1110', QtCore.QVariant('Right'), 0],
    ['b','ROCK_003_003_003_an_c001', '1001-1110', QtCore.QVariant('Right'), 0]
    ]
    '''
    #print parseCmd('E:\\rock_sq\\sq001\\sc001\\stereoCameraLeft\\c001', mod = 1)
    #print getFrames("1001-1010,1012-1014")
    print getFrames("1001")
    #print getFrames("1001-1010,1012-1014,1016,1020-1022")