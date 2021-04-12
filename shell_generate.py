# -*- coding: utf-8 -*-
"""
Created on Thu Apr  8 16:10:23 2021

@author: MR toad
"""

import os

rootpath = os.getcwd()
filepathlist = []
for (root,dirs,files) in os.walk(rootpath):
  for name in files:
    if name.endswith('inBin'):
      filepathlist.append(os.path.join(root,name))

filepath2 = []
filename = []

for elem in filepathlist:
  filepath2.append(elem[:-len('inBin')])
  filename.append(elem.split('\\')[-2])


for (ind,path) in enumerate(filepath2):
  with open(rootpath + '\\disassemble.sh','a') as f:
    f.write('arm-linux-gnueabi-objdump -D ' + filepathlist[ind] + ' > ' + './' + filename[ind] + '.txt' + '\n')


