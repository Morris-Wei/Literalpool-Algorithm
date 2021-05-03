# -*- coding: utf-8 -*-
"""
Created on Mon May  3 16:13:40 2021

@author: MR toad
"""

# pool类
import parse_code

class Pool():
  def __init__(self,startaddr,size,imagebase):
    self.startaddr = startaddr # 起始地址
    self.size = size # 大小字节
    self.endaddr = self.startaddr + size -1 # 结束地址
    self.blocksize = self.size/4 # 大小为字
    self.imagebase = imagebase # image偏移
    self.displaymod = 'virtual' #显示的是虚拟地址还是实际地址,默认是virtual
    
#    self.newstartaddr = 
#    self.newendaddr = 
  def displayMsg(self): #显示各种信息
    print('startaddr:',hex(self.startaddr),'size:',hex(self.size),'endaddr:',hex(self.endaddr))
    print('blocksize:',self.blocksize,'imagebase:',hex(self.imagebase))
    print('displaymod:',self.displaymod)
  
  def changedisplaymod(self): # 改变地址的显示格式
    assert self.displaymod == 'virtual' or self.displaymod == 'realoffset'
    if self.displaymod == 'virtual':
      self.displaymod = 'realoffset'
      self.startaddr -= self.imagebase
      self.endaddr -= self.imagebase
      print('addr change from virtual to realoffset')
    elif self.displaymod == 'realoffset':
      self.displaymod = 'virtual'
      self.startaddr += self.imagebase
      self.endaddr += self.imagebase
      print('addr change from readoffset to virtual')
      
  def modecheck(self,mode): # 转换mode
    assert mode == 'virtual' or mode == 'realoffset'
    if self.displaymod is not mode:
      self.changedisplaymod()
  
  def isInPool(self,addr,mode): # 判断地址是否在这个池中
    self.modecheck(mode)
    if addr >= self.startaddr and addr <= self.endaddr:
      return True
    else:
      return False
    
  def push(self,addr,mode): # 弹入最后一个，这里加addr是为了保险可以去掉
    self.modecheck(mode)
    if addr == self.endaddr + 4:
      self.endaddr = addr
      self.size += 4
      self.blocksize += 1
    else:
      print('Push Failed!!')
      
  def pop(self,mode): # 弹出最后一个
    self.modecheck(mode)
    if self.size != 0:
        self.endaddr -= 4
        self.size -= 4
        self.blocksize -= 1
    else:
      print('Pop Failed!!')
  
# 加上读写的函数
  
class literalPool(Pool):
  def __init__(self,startaddr,size,imagebase):
    super().__init__(startaddr,size,imagebase)
    self.changebit = 0 # 位置是否切换
    self.newstartaddr = 0 # 新起始的地址
    self.newendaddr = 0 # 新结束地址
#    self.type = '' # 由tail，head，mid三种类型，对应在func的尾部，头部，中间
     #所处函数块

  def displayMsg(self): #显示各种信息
    super().displayMsg()
    print('changed?:',self.changebit,'newstartaddr:',self.newstartaddr,'newendaddr',self.newendaddr)
    print('type:',self.type)

class codePool(Pool):
  def __init__(self,startaddr,size,imagebase):
    super().__init__(startaddr,size,imagebase)
    self.ldraddrlist = [] #在本codePool中ldr指令的地址集合
    self.changebit = 0 # 位置是否切换
    self.newstartaddr = 0 # 新起始的地址
    self.newendaddr = 0 # 新结束地址

  def wldrlist(self,addr,mode):
    self.modecheck(mode)
    isIn = self.isInPool(addr)
    if isIn:
      self.ldraddrlist.append(addr)
    
  def displayMsg(self): #显示各种信息
    super().displayMsg()
    print('changed?:',self.changebit,'newstartaddr:',self.newstartaddr,'newendaddr',self.newendaddr)
    print('ldraddrlist:',self.ldraddrlist)
    
def makeliteralpoollist(path):
  getLdr

if __name__ == '__main__':
  path = 'E:\pythonProject\assembly_code\bzip2.txt'
