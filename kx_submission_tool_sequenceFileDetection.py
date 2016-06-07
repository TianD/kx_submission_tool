#coding:utf-8
'''
Created on 2016年5月6日 下午2:59:15

@author: TianD

@E-mail: tiandao_dunjian@sina.cn

@Q    Q: 298081132

@Description:

'''
import difflib
import re
import os, os.path
###########################################################################################################
# 合成素材输出mov

ffmpegPath = os.path.join(os.path.dirname(__file__), 'ffmpeg.exe')
#sourse = 'E:\ffmpeg\eq001\sq002\sc009\c001\XFTL_001_002_009_cp_c001.10%02d.tga'
#convertCmd = 'xcopy {0} {1} /e /y \r\n'
convertCmd = '{0} -y -probesize 5000000 -f image2 -r 25 -i {1} -maxrate 7350000 -sc_threshold 1000000000 -qblur 0.3 -qcomp 0.7 -b:v 2.14748e+009 -c:v prores_ks -vendor apl0 -bits_per_mb 8192 -quant_mat 4 -profile:v 3 -pix_fmt:v yuva444p10le {2}\r\n'
#convertCmd = '{0} -y -probesize 5000000 -f image2 -r 25 -i {1} -maxrate 7350000 -sc_threshold 1000000000 -qblur 0.3 -qcomp 0.7 -b:v 2.14748e+009 -c:v prores_ks -vendor apl0 -bits_per_mb 8192 -quant_mat 4 -profile:v 4 -pix_fmt:v yuva444p10le {2}\r\n'

class SequenceFileDetection(object):
    """
    分析文件列表是否为序列文件
    """
    def __init__(self):
        super(SequenceFileDetection, self).__init__()
        # mode=0返回完整的数字序列
        # 适合渲染图片进行查询匹配使用
        self.sequenceDict1 = {}
        # mode=1返回不同部分的数字序列
        # 适合部分将序列贴图转换成视频格式插件使用
        self.sequenceDict2 = {}

        self.separateFiles = []               # 非序列的文件列表
        self.startFrame = -1                      # 设置起始帧
        self.endFrame = 0                       # 设置结束帧

    def _getFrontNumStr(self, str1=''):
        """获取字符串前端属于数字的字符"""
        numStr = ''
        current = 0
        while(str1):
            if str1[current].isdigit():
                numStr += str1[current]
                str1 = str1[1:]
            else:
                break
        return numStr

    def _getEndNumStr(self, str1=''):
        """获取字符串末尾属于数字的字符"""
        numStr = ''
        current = -1
        while(str1):
            if str1[current].isdigit():
                numStr = str1[current] + numStr
                str1 = str1[:-1]
            else:
                break
        return numStr

    def _sequenceSortKey(self, str1='', length=255):
        """
                序列文件列表排序的Key模块
        length为字符长度,一般windows文件名最长为255
        """
        strNum = ''.join(re.findall(r'\d', str1))
        str1 = ''.join(re.findall(r'\D', str1)) + strNum.zfill(length)
        return str1

    def _filesCompare(self, file1='', file2=''):
        """分析两个文件是否形成序列文件"""
        filesDict = []
        a = file1
        b = file2
        seq = difflib.SequenceMatcher(lambda x: x.isdigit(), a, b)
        k = 1
        switch = 0
        i3 = 0
        i4 = 0
        j3 = 0
        j4 = 0
        for tag, i1, i2, j1, j2 in seq.get_opcodes():
            if tag == 'replace':
                if 0 == k or 0 == i1 or 0 == j1 or not (a[i1:i2].isdigit() and b[j1:j2].isdigit()):
                    switch = 0
                    break
                switch = 1
                k -= 1
                i3 = i1
                i4 = i2
                j3 = j1
                j4 = j2

            if tag == 'delete':
                if 0 == k or i1 < 2 or not (a[i1:i2].isdigit() and a[i1-1:i1].isdigit()):
                    switch = 0
                    break
                switch = 1
                k -= 1
                i3 = i1-1
                i4 = i2
                j3 = j1-1
                j4 = j2

            if tag == 'insert':
                if 0 == k or j1 < 2 or not (b[j1:j2].isdigit() and b[j1-1:j1].isdigit()):
                    switch = 0
                    break
                switch = 1
                k -= 1
                i3 = i1-1
                i4 = i2
                j3 = j1-1
                j4 = j2

        if switch:
            i1 = i3
            i2 = i4
            j1 = j3
            j2 = j4
            temp = self._getEndNumStr(a[0:i1])
            i3 = i1 - len(temp)
            temp = self._getFrontNumStr(a[i2:])
            i4 = i2 + len(temp)

            temp = self._getEndNumStr(b[0:j1])
            j3 = j1 - len(temp)
            temp = self._getFrontNumStr(b[j2:])
            j4 = j2 + len(temp)

            if i3:
                filesDict = [
                        [a[0:i3]+'#'+a[i4:], a[i3:i4], b[j3:j4]],
                        [b[0:i1]+'%'+str(j4-j1)+'d'+b[j4:], a[i1:i4], b[j1:j4]]
                                ]
            else:
                filesDict = [
                        [a[0:i1]+'#'+a[i4:], a[i1:i4], b[j1:j4]],
                        [b[0:i1]+'%'+str(j4-j1)+'d'+b[j4:], a[i1:i4], b[j1:j4]]
                                ]
        else:
            filesDict = []
        return filesDict

    def _getMissList(self, frame1=0, frame2=0):
        """
        根据预设的起始帧和结束帧获取丢失帧列表
        """
        missList = []
        missList.extend(list(xrange(frame1, frame2)))
        return missList

    def _setResults(self, files1='', files2='', missList=[]):
        """将序列结果存入到预设的字典中"""
        results = self._filesCompare(files1, files2)
        if self.startFrame > -1:
            missList.extend(self._getMissList(self.startFrame, int(results[0][1])))
        if self.endFrame > 0:
            missList.extend(self._getMissList(int(results[0][2])+1, self.endFrame+1))
        missList.sort()
        self.sequenceDict1[results[0][0]] = [results[0][1], results[0][2], missList]
        self.sequenceDict2[results[1][0]] = [results[1][1], results[1][2], missList]

    def _filesAnalysis(self, files=[]):
        """递归分析多个文件列表是否形成序列文件"""
        if files:
            fileNum = len(files)
            if fileNum != 1:
                missList = []
                switch = 1
                temp = ''
                for i in xrange(1, fileNum):
                    results = self._filesCompare(files[i-1], files[i])
                    if results:
                        if temp:
                            if temp != results[0][0]:
                                switch = 0
                                i -= 1
                                break
                        else:
                            temp = results[0][0]
                        missList.extend(list(range(int(results[0][1])+1, int(results[0][2]))))
                    else:
                        switch = 0
                        break
                if switch:
                    self._setResults(files1=files[0], files2=files[i], missList=missList)
                    #results = self._filesCompare(files[0], files[i])
                    #self.sequenceDict1[results[0][0]] = [results[0][1], results[0][2], missList]
                    #self.sequenceDict2[results[1][0]] = [results[1][1], results[1][2], missList]
                else:
                    if i == 1:
                        self.separateFiles.append(files[0])
                    else:
                        self._setResults(files1=files[0], files2=files[i-1], missList=missList)
                        #results = self._filesCompare(files[0], files[i-1])
                        #self.sequenceDict1[results[0][0]] = [results[0][1], results[0][2], missList]
                        #self.sequenceDict2[results[1][0]] = [results[1][1], results[1][2], missList]
                    self._filesAnalysis(files[i:])
            else:
                self.separateFiles.append(files[0])

    def setSequenceFiles(self, files=[], startFrame=-1, endFrame=0):
        """
                设置需要分析的文件列表
        files 为文件列表
        startFrame 为预设的起始帧
        endFrame 为预设的结束帧
        """
        if startFrame > -1:
            self.startFrame = int(startFrame)
        if endFrame > 0:
            self.endFrame = int(endFrame)
        files = sorted(files, key=lambda str: self._sequenceSortKey(str))
        self._filesAnalysis(files)



    def getSequenceInfo(self, mode=0):
        """
        返回文件列表的分析结果
        输入(默认mode=0):
            mode=0返回完整的数字序列(适合查询)
            mode=1返回不同部分的数字序列(适合ffmpeg插件)
        输出(字典类型):
            keys=序列文件的文件名
            keys.values[0], 起始帧
            keys.values[1], 结束帧
            keys.values[2], 缺失的序列列表
            key='separateFiles',values=非序列文件列表
        """
        sequenceDict = {}
        if not mode:
            sequenceDict.update(self.sequenceDict1)
        else:
            sequenceDict.update(self.sequenceDict2)
        sequenceDict['separateFiles'] = self.separateFiles
        return sequenceDict

def conversionCmdPath(path=''):
    """将有空格的路径转换为cmd可以识别的路径"""
    path = os.path.normpath(path)
    pathList = []
    for path in path.split('\\'):
        if re.findall('\s+', path):
            pathList.append('\"'+path+'\"')
        else:
            pathList.append(path)
    path = '\\'.join(pathList)
    path = os.path.normpath(path)
    return path

def projFFmpeg(files=[], mode=1):
    """将序列文件转换成项目需要的ffmpeg格式"""
    fileName = []
    fileDict = {}
    projFile = SequenceFileDetection()
    projFile.setSequenceFiles(files)
    fileDict = projFile.getSequenceInfo(mode)
    for key in fileDict:
        if key != 'separateFiles' and not bool(fileDict[key][2]):
            if int(fileDict[key][0])==1:
                fileName.append(key)
            else:
                break
    return fileName

def convert(paths, dest, batName, batPath):
    if not os.path.exists(paths):
        return False
    
    if not os.path.exists(dest):
        try:
            os.makedirs(dest)
        except:
            return False
    
    if not os.path.exists(batPath):
        try:
            os.makedirs(batPath)
        except:
            return False
    
    fileNames = []
    badFilePath = []
    #f = open('%s\\ffmpeg.bat' % path_1, 'w+')
    f = open('%s\\%s.bat' % (batPath, batName), 'w+')
    for root, dirs, files in os.walk(paths):
        #path = os.path.join(root,filespath)
        if files:
            fileNames = projFFmpeg(files)
            if bool(fileNames) and len(fileNames) == 1: 
                sourse = root + '\\' + fileNames[0].replace('%', '%%', 1)
                destName = fileNames[0]
                destName = destName.split('.')[0]
                tempList = re.findall('cp_c{0,1}[0-9]{2,4}', destName)
                if tempList:
                    destName = destName.replace(tempList[0], 'cp', 1)
                destName += '.mov'
                destName = dest + '\\' + destName
                f.write(convertCmd.format(ffmpegPath, sourse, destName))
            else:
                badFilePath.append(root)
    if badFilePath:
        f.write('\r\n\r\n\r\nREM 文件不规范的路径:\r\n')
        for path1 in badFilePath:
            f.write('REM %s\r\n' % path1)
    #f.write('pause\r\n')
    f.close()
    print "create file ok"
    
    os.system(f.name)

if __name__ == "__main__":
    '''
    #paths = '\\\\kaixuan.com\\kx\\Proj\\Priject\\xuanfengtuoluo\\Production\\Render\\Comp\\EVEN\\ep020'
    #dest = '\\\\kaixuan.com\\kx\\Proj\\Priject\\xuanfengtuoluo\\Production\\Render\\Mov\\EVEN\\ep020_test\\'
    
    #paths = '\\\\kaixuan.com\\kx\\Proj\\Priject\\xuanfengtuoluo\\Production\\Render\\Comp\\EVEN\\ep010'
    #dest = '\\\\kaixuan.com\\kx\\Proj\\Priject\\xuanfengtuoluo\\Production\\Render\\Mov\\EVEN\\ep010_HQ\\'
    #batName = 'ffmpeg_ep010_HQ'
    
    #paths = '\\\\kaixuan.com\\kx\\Proj\\Priject\\xuanfengtuoluo\\Production\\Render\\Comp\\ODD\\ep021'
    #dest = '\\\\kaixuan.com\\kx\\Proj\\Priject\\xuanfengtuoluo\\Production\\Render\\Mov\\ODD\\ep021_HQ\\'
    
    
    
    #paths = '\\\\kaixuan.com\\kx\\Proj\\Priject\\xuanfengtuoluo\\Production\\Render\\Comp\\EVEN\\ep000\\sqSJG'
    #dest = '\\\\kaixuan.com\\kx\\Proj\\Priject\\xuanfengtuoluo\\Production\\Render\\Mov\\EVEN\\ep000\\'
    #batName = 'ffmpeg_ep000_HQ'
    
    
    #paths = '\\\\kaixuan.com\\kx\\Proj\\Priject\\xuanfengtuoluo\\Production\\Render\\Comp\\EVEN\\ep000\\sqPTQ'
    #dest = '\\\\kaixuan.com\\kx\\Proj\\Priject\\xuanfengtuoluo\\Production\\Render\\Mov\\EVEN\\ep000_PTQ\\'
    #batName = 'ffmpeg_ep000_PTQ_HQ'
    
    #paths = '\\\\kaixuan.com\\kx\\Proj\\Priject\\xuanfengtuoluo\\Production\\Render\\Comp\\EVEN\\ep010'
    #dest = '\\\\kaixuan.com\\kx\\Proj\\Priject\\xuanfengtuoluo\\Production\\Render\\Mov\\EVEN\\ep010\\'
    #batName = 'ffmpeg_ep010_HQ'
    
    #paths = '\\\\kaixuan.com\\kx\\Proj\\Priject\\xuanfengtuoluo\\Production\\Render\\Comp\\ODD\\ep021'
    #dest = '\\\\kaixuan.com\\kx\\Proj\\Priject\\xuanfengtuoluo\\Production\\Render\\Mov\\ODD\\ep021\\'
    #batName = 'ffmpeg_ep021_HQ'
    
    #paths = '\\\\kaixuan.com\\kx\\Proj\\Priject\\xuanfengtuoluo\\Production\\Render\\Comp\\EVEN\\ep000\\sqSJG'
    #dest = '\\\\kaixuan.com\\kx\\Proj\\Priject\\xuanfengtuoluo\\Production\\Render\\Mov\\EVEN\\ep000\\ep000_SJG\\'
    #batName = 'ffmpeg_ep000_SJG_HQ'
    
    #paths = '\\\\kaixuan.com\\kx\\Proj\\Priject\\xuanfengtuoluo\\Production\\Render\\Comp\\EVEN\\ep000\\sqPTQ'
    #dest = '\\\\kaixuan.com\\kx\\Proj\\Priject\\xuanfengtuoluo\\Production\\Render\\Mov\\EVEN\\ep000\\ep000_PTQ\\'
    #batName = 'ffmpeg_ep000_PTQ_HQ_001'
    
    #paths = '\\\\kaixuan.com\\kx\\Proj\\Priject\\xuanfengtuoluo\\Production\\Render\\Comp\\EVEN\\ep010'
    #dest = '\\\\kaixuan.com\\kx\\Proj\\Priject\\xuanfengtuoluo\\Production\\Render\\Mov\\EVEN\\ep010\\xiugai\\0821\\'
    #batName = 'ffmpeg_ep010_HQ_xiu0821'
    
    #paths = '\\\\kaixuan.com\\kx\\Proj\\Priject\\xuanfengtuoluo\\Production\\Render\\Comp\\EVEN\\ep000\\sqPTQ'
    #dest = '\\\\kaixuan.com\\kx\\Proj\\Priject\\xuanfengtuoluo\\Production\\Render\\Mov\\EVEN\\ep000\\ep000_PTQ\\'
    #batName = 'ffmpeg_ep000_PTQ_HQ_0824'
    
    
    #paths = '\\\\kaixuan.com\\kx\\Proj\\Priject\\xuanfengtuoluo\\Production\\Render\\Comp\\ODD\\ep021\\sq003a\\sc046\\c001'
    #dest = '\\\\kaixuan.com\\kx\\Proj\\Priject\\xuanfengtuoluo\\Production\\Render\\Mov\\ODD\\ep021\\fanxiu\\'
    #batName = 'ffmpeg_ep021_HQ_xiugai_sq003a_sc046'
    
    #paths = '\\\\kaixuan.com\\kx\\Proj\\Priject\\xuanfengtuoluo\\Production\\Render\\Comp\\EVEN\\ep022'
    #dest = '\\\\kaixuan.com\\kx\\Proj\\Priject\\xuanfengtuoluo\\Production\\Render\\Mov\\EVEN\\ep022\\'
    #batName = 'ffmpeg_ep022_HQ'
    
    #paths = '\\\\kaixuan.com\\kx\\Proj\\Priject\\xuanfengtuoluo\\Production\\Render\\Comp\\EVEN\\ep020'
    #dest = '\\\\kaixuan.com\\kx\\Proj\\Priject\\xuanfengtuoluo\\Production\\Render\\Mov\\EVEN\\ep020\\'
    #batName = 'ffmpeg_ep020_HQ'
    
    #paths = '\\\\kaixuan.com\\kx\\Proj\\Priject\\xuanfengtuoluo\\Production\\Render\\Comp\\EVEN\\ep020\\sq003b\\sc040'
    #dest = '\\\\kaixuan.com\\kx\\Proj\\Priject\\xuanfengtuoluo\\Production\\Render\\Mov\\EVEN\\ep020\\'
    #batName = 'ffmpeg_ep020_HQ_sq003b_sc040'
    
    #paths = '\\\\kaixuan.com\\kx\\Proj\\Priject\\xuanfengtuoluo\\Production\\Render\\Comp\\EVEN\\ep000\\sqPWQ'
    #dest = '\\\\kaixuan.com\\kx\\Proj\\Priject\\xuanfengtuoluo\\Production\\Render\\Mov\\EVEN\\ep000\\ep000_PWQ\\'
    #batName = 'ffmpeg_ep000_PWQ_HQ_001'
    
    
    #paths = '\\\\kaixuan.com\\kx\\Proj\\Priject\\xuanfengtuoluo\\Production\\Render\\Comp\\EVEN\\ep000\\sqPWQ\\sc021'
    #dest = '\\\\kaixuan.com\\kx\\Proj\\Priject\\xuanfengtuoluo\\Production\\Render\\Mov\\EVEN\\ep000\\ep000_PWQ\\'
    #batName = 'ffmpeg_ep000_PWQ_HQ_001_021'
    
    
    #paths = '\\\\kaixuan.com\\kx\\Proj\\Priject\\xuanfengtuoluo\\Production\\Render\\Comp\\EVEN\\ep000\\sqPWQ\\sc023'
    #dest = '\\\\kaixuan.com\\kx\\Proj\\Priject\\xuanfengtuoluo\\Production\\Render\\Mov\\EVEN\\ep000\\ep000_PWQ\\'
    #batName = 'ffmpeg_ep000_PWQ_HQ_001_023'
    
    #paths = '\\\\kaixuan.com\\kx\\Proj\\Priject\\xuanfengtuoluo\\Production\\Render\\Comp\\ODD\\ep029'
    #dest = '\\\\kaixuan.com\\kx\\Proj\\Priject\\xuanfengtuoluo\\Production\\Render\\Mov\\ODD\\ep029\\'
    #batName = 'ffmpeg_ep029_HQ_xiu02'
    
    
    #paths = '\\\\kaixuan.com\\kx\\Proj\\Priject\\xuanfengtuoluo\\Production\\Render\\Comp\\EVEN\\ep030'
    #dest = '\\\\kaixuan.com\\kx\\Proj\\Priject\\xuanfengtuoluo\\Production\\Render\\Mov\\EVEN\\ep030\\'
    #batName = 'ffmpeg_ep030_HQ'
    
    #paths = '\\\\kaixuan.com\\kx\\Proj\\Priject\\xuanfengtuoluo\\Production\\Render\\Comp\\ODD\\ep999'
    #dest = '\\\\kaixuan.com\\kx\\Proj\\Priject\\xuanfengtuoluo\\Production\\Render\\Mov\\ODD\\ep999\\0907\\'
    #batName = 'ffmpeg_ep999_HQ_002'
    
    #paths = '\\\\kaixuan.com\\kx\\Proj\\Priject\\xuanfengtuoluo\\Production\\Render\\Comp\\ODD\\ep039'
    #dest = '\\\\kaixuan.com\\kx\\Proj\\Priject\\xuanfengtuoluo\\Production\\Render\\Mov\\ODD\\ep039\\'
    #batName = 'ffmpeg_ep039_HQ_20150908'
    
    #paths = '\\\\kaixuan.com\\kx\\Proj\\Priject\\xuanfengtuoluo\\Production\\Render\\Comp\\EVEN\\ep000\\sqPTQ'
    #dest = '\\\\kaixuan.com\\kx\\Proj\\Priject\\xuanfengtuoluo\\Production\\Render\\Mov\\EVEN\\ep000\\ep000_PTQ\\'
    #batName = 'ffmpeg_ep000_PTQ_HQ_0907'
    
    #paths = '\\\\kaixuan.com\\kx\\Proj\\Priject\\xuanfengtuoluo\\Production\\Render\\Comp\\EVEN\\ep036'
    #dest = '\\\\kaixuan.com\\kx\\Proj\\Priject\\xuanfengtuoluo\\Production\\Render\\Mov\\EVEN\\ep036\\'
    #batName = 'ffmpeg_ep036_HQ_20150907'
    
    #paths = '\\\\kaixuan.com\\kx\\Proj\\Priject\\xuanfengtuoluo\\Production\\Render\\Comp\\EVEN\\ep000\\sqSJG'
    #dest = '\\\\kaixuan.com\\kx\\Proj\\Priject\\xuanfengtuoluo\\Production\\Render\\Mov\\EVEN\\ep000\\ep000_SJG\\'
    #batName = 'ffmpeg_ep000_SJG_HQ_20150909'
    
    #paths = '\\\\kaixuan.com\\kx\\Proj\\Priject\\xuanfengtuoluo\\Production\\Render\\Comp\\EVEN\\ep000\\sqPWQ'
    #dest = '\\\\kaixuan.com\\kx\\Proj\\Priject\\xuanfengtuoluo\\Production\\Render\\Mov\\EVEN\\ep000\\ep000_PWQ\\'
    #batName = 'ffmpeg_ep000_PWQ_HQ_20150909'
    
    #paths = '\\\\kaixuan.com\\kx\\Proj\\Priject\\xuanfengtuoluo\\Production\\Render\\Comp\\ODD\\ep999'
    #dest = '\\\\kaixuan.com\\kx\\Proj\\Priject\\xuanfengtuoluo\\Production\\Render\\Mov\\ODD\\ep999\\0907\\'
    #batName = 'ffmpeg_ep999_HQ_004'
    
    #paths = '\\\\kaixuan.com\\kx\\Proj\\Priject\\xuanfengtuoluo\\Production\\Render\\Comp\\EVEN\\ep000\\sqPTQ\\sc013k\\c003'
    #dest = '\\\\kaixuan.com\\kx\\Proj\\Priject\\xuanfengtuoluo\\Production\\Render\\Mov\\EVEN\\ep000\\ep000_PTQ\\20150911\\'
    #batName = 'ffmpeg_ep000_PTQ_sc013k'
    
    #paths = '\\\\kaixuan.com\\kx\\Proj\\Priject\\xuanfengtuoluo\\Production\\Render\\Comp\\EVEN\\ep000\\sqPWQ\\sc004\\c002'
    #dest = '\\\\kaixuan.com\\kx\\Proj\\Priject\\xuanfengtuoluo\\Production\\Render\\Mov\\EVEN\\ep000\\ep000_PWQ\\20150911\\'
    #batName = 'ffmpeg_ep000_PWQ_sc004'
    
    #paths = '\\\\kaixuan.com\\kx\\Proj\\Priject\\xuanfengtuoluo\\Production\\Render\\Comp\\ODD\\ep029'
    #dest = '\\\\kaixuan.com\\kx\\Proj\\Priject\\xuanfengtuoluo\\Production\\Render\\Mov\\ODD\\ep029\\20150911\\'
    #batName = 'ffmpeg_ep029_HQ_20150911'
    
    #paths = '\\\\kaixuan.com\\kx\\Proj\\Priject\\xuanfengtuoluo\\Production\\Render\\Comp\\EVEN\\ep030'
    #dest = '\\\\kaixuan.com\\kx\\Proj\\Priject\\xuanfengtuoluo\\Production\\Render\\Mov\\EVEN\\ep030\\'
    #batName = 'ffmpeg_ep030_HQ_20150911'
    
    #paths = '\\\\kaixuan.com\\kx\\Proj\\Priject\\xuanfengtuoluo\\Production\\Render\\Comp\\EVEN\\ep036'
    #dest = '\\\\kaixuan.com\\kx\\Proj\\Priject\\xuanfengtuoluo\\Production\\Render\\Mov\\EVEN\\ep036\\'
    #batName = 'ffmpeg_ep036_HQ_20150911'
    
    #paths = '\\\\kaixuan.com\\kx\\Proj\\Priject\\xuanfengtuoluo\\Production\\Render\\Comp\\ODD\\ep039'
    #dest = '\\\\kaixuan.com\\kx\\Proj\\Priject\\xuanfengtuoluo\\Production\\Render\\Mov\\ODD\\ep039\\'
    #batName = 'ffmpeg_ep039_HQ_20150911'
    
    #paths = '\\\\kaixuan.com\\kx\\Proj\\Priject\\xuanfengtuoluo\\Production\\Render\\Comp\\ODD\\ep999'
    #dest = '\\\\kaixuan.com\\kx\\Proj\\Priject\\xuanfengtuoluo\\Production\\Render\\Mov\\ODD\\ep999\\0907\\'
    #batName = 'ffmpeg_ep999_HQ_20150911'
    
    #paths = '\\\\kaixuan.com\\kx\\Proj\\Priject\\xuanfengtuoluo\\Production\\Render\\Comp\\EVEN\\ep030\\sq003b\\sc028\\c001'
    #dest = '\\\\kaixuan.com\\kx\\Proj\\Priject\\xuanfengtuoluo\\Production\\Render\\Mov\\EVEN\\ep030\\20150912\\'
    #batName = 'ffmpeg_ep030_sq003b_sc028_HQ_20150912'
    
    #paths = '\\\\kaixuan.com\\kx\\Proj\\Priject\\xuanfengtuoluo\\Production\\Render\\Comp\\ODD\\ep999\\sqTF6'
    #dest = '\\\\kaixuan.com\\kx\\Proj\\Priject\\xuanfengtuoluo\\Production\\Render\\Mov\\ODD\\ep999\\0907\\'
    #batName = 'ffmpeg_ep999_sqTF6_HQ_20150914'
    
    #paths = '\\\\kaixuan.com\\kx\\Proj\\Priject\\xuanfengtuoluo\\Production\\Render\\Comp\\EVEN\\ep000\\sqXBT\\sc001\\c001'
    #dest = 'F:\\rend\\ep000\\'
    #batName = 'ffmpeg_ep000_XBT_sc001'
    
    #paths = '\\\\kaixuan.com\\kx\\Proj\\Priject\\xuanfengtuoluo\\Production\\Render\\Comp\\ODD\\ep999'
    #dest = '\\\\kaixuan.com\\kx\\Proj\\Priject\\xuanfengtuoluo\\Production\\Render\\Mov\\ODD\\ep999\\0907\\'
    #batName = 'ffmpeg_ep999_HQ_20150914'
    
    #paths = '\\\\kaixuan.com\\kx\\Proj\\Priject\\xuanfengtuoluo\\Production\\Render\\Comp\\ODD\\ep037'
    #dest = '\\\\kaixuan.com\\kx\\Proj\\Priject\\xuanfengtuoluo\\Production\\Render\\Mov\\ODD\\ep037\\'
    #batName = 'ffmpeg_ep037_HQ_20150915'
    
    #paths = '\\\\kaixuan.com\\kx\\Proj\\Priject\\xuanfengtuoluo\\Production\\Render\\Comp\\EVEN\\ep038'
    #dest = '\\\\kaixuan.com\\kx\\Proj\\Priject\\xuanfengtuoluo\\Production\\Render\\Mov\\EVEN\\ep038\\'
    #batName = 'ffmpeg_ep038_HQ_20150915'
    
    #paths = '\\\\kaixuan.com\\kx\\Proj\\Priject\\xuanfengtuoluo\\Production\\Render\\Comp\\ODD\\ep035'
    #dest = '\\\\kaixuan.com\\kx\\Proj\\Priject\\xuanfengtuoluo\\Production\\Render\\Mov\\ODD\\ep035\\'
    #batName = 'ffmpeg_ep035_HQ_20150916'
    
    #paths = '\\\\kaixuan.com\\kx\\Proj\\Priject\\xuanfengtuoluo\\Production\\Render\\Comp\\EVEN\\ep040'
    #dest = '\\\\kaixuan.com\\kx\\Proj\\Priject\\xuanfengtuoluo\\Production\\Render\\Mov\\EVEN\\ep040\\'
    #batName = 'ffmpeg_ep040_HQ_20150917'
    
    #paths = '\\\\kaixuan.com\\kx\\Proj\\Priject\\xuanfengtuoluo\\Production\\Render\\Comp\\EVEN\\ep040\\sq001a\\sc033\\c001'
    #dest = '\\\\kaixuan.com\\kx\\Proj\\Priject\\xuanfengtuoluo\\Production\\Render\\Mov\\EVEN\\ep040\\'
    #batName = 'ffmpeg_ep040_001a_033_HQ_20150917'
    
    #paths = '\\\\kaixuan.com\\kx\\Proj\\Priject\\xuanfengtuoluo\\Production\\Render\\Comp\\ODD\\ep039\sq003\\sc095\\c001'
    #dest = '\\\\kaixuan.com\\kx\\Proj\\Priject\\xuanfengtuoluo\\Production\\Render\\Mov\\ODD\\ep039\\'
    #batName = 'ffmpeg_ep039_003_095_HQ_20150917'
    
    #paths = '\\\\kaixuan.com\\kx\\Proj\\Priject\\xuanfengtuoluo\\Production\\Render\\Comp\\EVEN\\ep038\\sq006\\sc026\\c003'
    #dest = '\\\\kaixuan.com\\kx\\Proj\\Priject\\xuanfengtuoluo\\Production\\Render\\Mov\\EVEN\\ep038\\fanxiu\\'
    #batName = 'ffmpeg_ep038_HQ_20150917_07'
    
    #paths = '\\\\kaixuan.com\\kx\\Proj\\Priject\\xuanfengtuoluo\\Production\\Render\\Comp\\EVEN\\ep040'
    #dest = '\\\\kaixuan.com\\kx\\Proj\\Priject\\xuanfengtuoluo\\Production\\Render\\Mov\\EVEN\\ep040\\'
    #batName = 'ffmpeg_ep040_HQ_20150918'
    
    #paths = '\\\\kaixuan.com\\kx\\Proj\\Priject\\xuanfengtuoluo\\Production\\Render\\Comp\\ODD\\ep999'
    #dest = '\\\\kaixuan.com\\kx\\Proj\\Priject\\xuanfengtuoluo\\Production\\Render\\Mov\\ODD\\ep999\\0918shenji\\'
    #batName = 'ffmpeg_ep999_HQ_20150918'
    
    #paths = '\\\\kaixuan.com\\kx\\Proj\\Priject\\xuanfengtuoluo\\Production\\Render\\Comp\\ODD\\ep999\\sqTF3\\sc004s\\c001'
    #dest = '\\\\kaixuan.com\\kx\\Proj\\Priject\\xuanfengtuoluo\\Production\\Render\\Mov\\ODD\\ep999\\0918shenji\\'
    #batName = 'ffmpeg_ep999_sqTF3_HQ_20150918'
    
    #paths = '\\\\kaixuan.com\\kx\\Proj\\Priject\\xuanfengtuoluo\\Production\\Render\\Comp\\ODD\\ep027'
    #dest = '\\\\kaixuan.com\\kx\\Proj\\Priject\\xuanfengtuoluo\\Production\\Render\\Mov\\ODD\\ep027\\'
    #batName = 'ffmpeg_ep027_HQ_20150918'
    
    #paths = '\\\\kaixuan.com\\kx\\Proj\\Priject\\xuanfengtuoluo\\Production\\Render\\Comp\\ODD\\ep027'
    #dest = '\\\\kaixuan.com\\kx\\Proj\\Priject\\xuanfengtuoluo\\Production\\Render\\Mov\\ODD\\ep027\\'
    #batName = 'ffmpeg_ep027_HQ_20150918'
    
    #paths = '\\\\kaixuan.com\\kx\\Proj\\Priject\\xuanfengtuoluo\\Production\\Render\\Comp\\ODD\\ep017\\sq007\\sc009'
    #dest = '\\\\kaixuan.com\\kx\\Proj\\Priject\\xuanfengtuoluo\\Production\\Render\\Mov\\ODD\\ep017\\0921\\'
    #batName = 'ffmpeg_ep017_007_009_HQ_20150921'
    
    #paths = '\\\\kaixuan.com\\kx\\Proj\\Priject\\xuanfengtuoluo\\Production\\Render\\Comp\\ODD\\ep017\\sq008\\sc010'
    #dest = '\\\\kaixuan.com\\kx\\Proj\\Priject\\xuanfengtuoluo\\Production\\Render\\Mov\\ODD\\ep017\\0921\\'
    #batName = 'ffmpeg_ep017_008_010_HQ_20150921'
    
    #paths = '\\\\kaixuan.com\\kx\\Proj\\Priject\\xuanfengtuoluo\\Production\\Render\\Comp\\ODD\\ep017\\sq006\\sc007'
    #dest = '\\\\kaixuan.com\\kx\\Proj\\Priject\\xuanfengtuoluo\\Production\\Render\\Mov\\ODD\\ep017\\0921\\'
    #batName = 'ffmpeg_ep017_006_007_HQ_20150921'
    
    #paths = '\\\\kaixuan.com\\kx\\Proj\\Priject\\xuanfengtuoluo\\Production\\Render\\Comp\\EVEN\\ep000\\sqXBT'
    #dest = '\\\\kaixuan.com\\kx\\Proj\\Priject\\xuanfengtuoluo\\Production\\Render\\Mov\\EVEN\\ep000\\ep000_XBT\\'
    #batName = 'ffmpeg_ep000_XBT_HQ_0925'
    
    #paths = '\\\\kaixuan.com\\kx\\Proj\\Priject\\xuanfengtuoluo\\Production\\Render\\Comp\\EVEN\\ep000\\sqXBT\\sc009\\c001'
    #dest = '\\\\kaixuan.com\\kx\\Proj\\Priject\\xuanfengtuoluo\\Production\\Render\\Mov\\EVEN\\ep000\\ep000_XBT\\'
    #batName = 'ffmpeg_ep000_009_XBT_HQ_0925'
    
    # paths = '\\\\kaixuan.com\\kx\\Proj\\Priject\\xuanfengtuoluo\\Production\\Render\\Comp\\EVEN\\ep028'
    # dest = '\\\\kaixuan.com\\kx\\Proj\\Priject\\xuanfengtuoluo\\Production\\Render\\Mov\\EVEN\\ep028\\'
    # batName = 'ffmpeg_ep028_HQ_20150925'
    '''
    ''
    paths = 'E:\\senba_sq\\sq001'
    dest = 'E:\\senba_mov\\sq001\\'
    batName = 'ffmpeg_sq001_HQ_20160509'
    path_1 = 'E:\\rend'
    convert(paths, dest, batName, path_1)