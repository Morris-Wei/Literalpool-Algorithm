# -*- coding: utf-8 -*-
"""
Created on Tue May  4 20:41:35 2021

@author: MR toad
"""
import pickle
from poolclass import *
from collections import deque

def list2Deque(literalpoolList, codepoolList):
    literalpoolDeque = deque(literalpoolList)
    codepoolDeque = deque(codepoolList)
    return literalpoolDeque,codepoolDeque

def relocate(codepoolDeque,sectioninfo):
    lptmpdeque = deque([])
    relocatedeque = deque([])
    ct = 0
    codepoolcount = len(codepoolDeque)
    while ct < codepoolcount:
        relocatedequesize = 0 # 已拍code的大小，单位字
        codepoolobj = codepoolDeque.popleft()
        if len(codepoolobj.lpstatus) == 1 and codepoolobj.lpstatus[0] == '111': # 可直接用
            if relocatedequesize + codepoolobj.blocksize < 1024:
                if ct == len(codepoolDeque) - 1: # 最后一个
                    relocatedeque.append(codepoolobj)
                    codepoolobj.changebit = 1  # 表示位置被变换过了
                    lptmpdeque.append(codepoolobj.lplist[0])
                    popAllFromlptmpDeque(lptmpdeque, relocatedeque)
                else:
                    relocatedeque.append(codepoolobj)
                    codepoolobj.changebit = 1  # 表示位置被变换过了
                    lptmpdeque.append(codepoolobj.lplist[0])
                    relocatedequesize += codepoolobj.blocksize
            else:
                popAllFromlptmpDeque(lptmpdeque, relocatedeque)
                relocatedequesize = 0
                relocatedeque.append(codepoolobj)
                lptmpdeque.append(codepoolobj.lplist[0])
                relocatedequesize += codepoolobj.blocksize
        elif len(codepoolobj.lpstatus) == 0: # 无常量池
            popAllFromlptmpDeque(lptmpdeque, relocatedeque)
            relocatedequesize = 0
            relocatedeque.append(codepoolobj)
            relocatedequesize += codepoolobj.blocksize
        else: # 常量池不止一个，或是常量池在上面
            popAllFromlptmpDeque(lptmpdeque, relocatedeque)
            relocatedequesize = 0
            uplist,downlist = getUpDownlplist(codepoolobj)
            for uplp in uplist:
                if uplp.changebit == 0: # 判断重要，表示uplp是否已经被重排，原因是该lp被前面的代码池所引用
                    uplp.changebit = 1
                    relocatedeque.append(uplp)
            relocatedeque.append(codepoolobj)
            codepoolobj.changebit = 1
            for downlp in downlist:
                if downlp.changebit == 0:
                    downlp.changebit = 1
                    relocatedeque.append(downlp)
        ct += 1
    resetchangedaddr(relocatedeque, sectioninfo)
    return relocatedeque

def getUpDownlplist(codepoolobj): # 得到在上面的，下面的常量池
    downlist = []
    uplist = []
    for id,lp in enumerate(codepoolobj.lplist):
        if codepoolobj.lpstatus[id][0] == '1':
            downlist.append(lp)
        else:
            uplist.append(lp)
    return uplist,downlist

def popAllFromlptmpDeque(lptmpdeque,relocatedeque):
    for i in range(len(lptmpdeque)):
        lp_t = lptmpdeque.popleft()
        if lp_t.changebit == 0:
            lp_t.changebit = 1
            relocatedeque.append(lp_t)

def resetchangedaddr(relocatedeque,sectioninfo):
    for id, pool in enumerate(relocatedeque):
        if id == 0:
            pool.newstartaddr = eval('0x' + sectioninfo['.text'][0])
        else:
            pool.newstartaddr = relocatedeque[id-1].newendaddr + 1
        pool.newendaddr = pool.newstartaddr + pool.size - 1

if __name__ == '__main__':
    with open('literalpoolList.pkl','rb') as f1:
        literalpoolList = pickle.load(f1)

    with open('codepoolList.pkl','rb') as f2:
        codepoolList = pickle.load(f2)

    literalpoolDeque, codepoolDeque = list2Deque(literalpoolList, codepoolList)


    with open('E:\pythonProject\secdict.pkl', 'rb') as f:
        sectioninfo = pickle.load(f)

    relocatedeque = relocate(codepoolDeque,sectioninfo)
    c = 0
