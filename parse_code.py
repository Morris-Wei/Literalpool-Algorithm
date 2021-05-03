# -*- coding: utf-8 -*-
"""
Created on Sat Apr 10 20:40:04 2021

@author: MR toad
"""
import os
import re
import matplotlib.pyplot as plt
#import pickle

start = 0x8170
end = 0x7c834


def getLdrLocation(txtpath): # 得到.text中所有含ldr指令列表
  ldr_list = []
  with open(txtpath,'r',encoding='utf-8') as f:
    while(True):
      str_t = f.readline()
      if not str_t:
        break
      if str_t.find('ldr')!= -1 and str_t.find('pc') != -1:
        addr = eval('0x' + str_t.strip().split(':')[0])
        if addr >= start and addr< end:
          ldr_list.append(str_t)
  return ldr_list


def cleaningList(ldr_list): # 清洗掉无关的数据
  pt1 = r'.*ldr.*\[pc.*\]\s;.*<.*>'
  for insstr in ldr_list:
    if insstr.find('<UNPREDICTABLE>') != -1: # 取消掉不可预测的
      ldr_list.remove(insstr)
      continue
    mt = re.search(pt1,insstr)
    if not mt:
      ldr_list.remove(insstr)
  return ldr_list


def printLdrType(ldr_list):# 打印所有LDR类型及其多少，主要是条件码的不同
  pt2 = r'ldr[a-z]*'
  type_dict = {}
  for ldrstr in ldr_list:
    mt = re.search(pt2,ldrstr)
    if mt:
      if mt.group(0) not in type_dict:
        type_dict[mt.group(0)] = 1
      else:
        type_dict[mt.group(0)] += 1
  return type_dict

def drawLdrTypeCnt(type_dict): # 画出不同LDR类型的多少
  xlist = []
  ylist = []
  for (k,v) in type_dict.items():
    xlist.append(k)
    ylist.append(v)
  plt.bar(xlist,ylist)
  plt.xticks(rotation=90)
  # plt.savefig(r".\InstructionTypeNumber.png")
  plt.show()

def getLdr2Literal(path):
  ins_list = getLdrLocation(path)
  cleaningList(ins_list)
  Ldr2Literal = {}
  pt3 = r'\w*:'
  pt4 = r';\s\w*\s<'
  for ins in ins_list:
    mt3 = re.search(pt3,ins)
    mt4 = re.search(pt4,ins)
    if mt3 and mt4:
      ldr_v_addr = mt3.group(0).replace(' ','')[:-1]
      tmp = mt4.group(0).replace(' ','')
      literal_v_addr = tmp[1:-1]
      Ldr2Literal[ldr_v_addr] = literal_v_addr
      
  return Ldr2Literal

def getliteral2Ldr(ldr2Literal):
  literal2Ldr = {}
  for k,v in ldr2Literal.items():
    literal2Ldr[v] = []
    literal2Ldr[v].append(k)
  return literal2Ldr

def writeDict(dictobj,path):
  with open(path,'w') as f:
    for k,v in dictobj.items():
      str_tmp = str(k) + ':' + str(v) + '\n'
      f.write(str_tmp)
      

#%%
if __name__ == '__main__':
  path = r'E:\pythonProject\assembly_code\bzip2.txt'
  
  ldr2Literal = getLdr2Literal(path)
  literal2Ldr = getliteral2Ldr(ldr2Literal)
  writeDict(ldr2Literal,'ldr2Literal.txt')
  writeDict(literal2Ldr,'literal2Ldr.txt')
#%%

