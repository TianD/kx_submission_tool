#coding:utf-8
'''
Created on 2016年6月13日 下午2:56:41

@author: TianD

@E-mail: tiandao_dunjian@sina.cn

@Q    Q: 298081132

@Description:

'''
#! /usr/bin/env python
#-----------------------------------------------------------------------------
# Copyright (c) 2013, PyInstaller Development Team.
#
# Distributed under the terms of the GNU General Public License with exception
# for distributing bootloader.
#
# The full license is in the file COPYING.txt, distributed with this software.
#-----------------------------------------------------------------------------
"""
Main command-line interface to PyInstaller.
"""
# from  PyInstaller import  *
import  os

if __name__ == '__main__':
    from PyInstaller.main import run
    opts=['showUI.py', '-D', '-w', '-nKX_submission_tool', '-iE:\\Scripts\\Eclipse\\kx_submission_tool\\kx_submission_tool.ico']
    #opts=['KX_Seq2Mov.spec', '-y']
    run(opts)