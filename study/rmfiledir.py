#!/usr/bin/python3

import os, sys
import shutil

# 列出目录
print ("目录为: %s" %os.listdir(os.getcwd()))

# 移除文件
# os.remove("aa.txt")
# os.removedirs("aa/bb/aa")
shutil.rmtree("aa")
# 移除后列出目录
print ("移除后 : %s" %os.listdir(os.getcwd()))