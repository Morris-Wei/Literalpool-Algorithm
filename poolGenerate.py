# -*- coding: utf-8 -*-
"""
Created on Tue May  4 09:05:20 2021

@author: MR toad
"""

import poolclass
import parse_code
import pickle

def getLdrLiteral(path):
  ldr2Literal = parse_code.getLdr2Literal(path)
  literal2Ldr = parse_code.getliteral2Ldr(ldr2Literal)
  return ldr2Literal,literal2Ldr

def makeLiteralPoolList(sectioninfo,ldr2Literal,literal2Ldr):
  codeaddrList = [] #存放代码指令地址
  literaladdrList = []
  literalpoolList = [] #存放literalpool对象的列表
  codepoolList = [] #存放codepool对象的列表
  ldrList = [] # ldr指令地址列表
  textstart = eval('0x' + sectioninfo['.text'][0])
  textsize = eval('0x' + sectioninfo['.text'][2])
  textend = textstart + textsize
  imagebase = textstart - eval('0x' + sectioninfo['.text'][1])
  for literaladdr in literal2Ldr.keys():
    addr_t = eval('0x' + literaladdr)
    literaladdrList.append(addr_t)
  for wordaddr in range(textstart,textend,4):
    if wordaddr not in literaladdrList:
      codeaddrList.append(wordaddr)
  
  
  for ldraddr in ldr2Literal.keys(): # 生成ldr指令地址列表
    addr_t = eval('0x' + ldraddr)
    ldrList.append(addr_t)
    
  ldrmem = []
  for i,v in enumerate(codeaddrList):
    if v in ldrList: # 记录ldr指令
      ldrmem.append(v)
    if i == 0:
      phead_ind = 0 # 头针
      phead_val = v
      ptail_ind = 0 # 尾针
      ptail_val = v
    else:
        if v == ptail_val + 4:
          ptail_val = v
          ptail_ind = i
        else:
          codepoolobj = poolclass.codePool(phead_val,v - phead_val,imagebase)
          codepoolobj.ldraddrlist = ldrmem[:] #深拷贝
          ldrmem.clear()
          codepoolList.append(codepoolobj)
          phead_ind = ptail_ind = i
          phead_val = ptail_val = v
  
  for i,v in enumerate(literaladdrList):
    if i == 0:
      phead_ind = 0 # 头针
      phead_val = v
      ptail_ind = 0 # 尾针
      ptail_val = v
    else:
        if v == ptail_val + 4:
          ptail_val = v
          ptail_ind = i
        else:
          literalpoolList.append(poolclass.literalPool(phead_val,v - phead_val,imagebase))
          phead_ind = ptail_ind = i
          phead_val = ptail_val = v
  
  return literalpoolList,codepoolList

def writecodepoollplist(literalpoolList,codepoolList,ldr2Literal):
  for codePoolObj in codepoolList:
    for ldraddr in codePoolObj.ldraddrlist:
      for literalpoolObj in literalpoolList:
        literaladdr_t = ldr2Literal[hex(ldraddr)[2:]]
        literaladdr = eval('0x' + literaladdr_t)
        if literalpoolObj.isInPool(literaladdr,'virtual') and literalpoolObj not in codePoolObj.lplist:
          codePoolObj.lplist.append(literalpoolObj)

if __name__ == '__main__':
  with open('E:\pythonProject\secdict.pkl','rb') as f:
    sectioninfo = pickle.load(f)
  path = r'E:\pythonProject\assembly_code\bzip2.txt'
  ldr2Literal,literal2Ldr = getLdrLiteral(path)
  literalpoolList,codepoolList = makeLiteralPoolList(sectioninfo,ldr2Literal,literal2Ldr)
  # c = 0
  # for k,v in ldr2Literal.items():
  #   k1 = eval('0x' + k)
  #   v1 = eval('0x' + v)
  #   if v1 <= k1:
  #     print(k,':',v)
  