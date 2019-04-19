import sys
import os
import json
import chardet

def ensure_file_exists(file_name):
    if (not os.path.exists(file_name)) or (not os.path.isfile(file_name)):
        print("File '{}' not found!".format(file_name))
        exit()

def ensure_dir_exists(dir_path):
    if (not os.path.exists(dir_path)) or os.path.isfile(dir_path):
        print("Dir '{}' not found!".format(dir_path))
        exit()

__capital="aeiou"
def is_capital(st):
    for c in __capital:
        if st.startswith(c):
            return True
    return False

__encoding_list=[None,"gbk","utf-8"]
def get_encoding(file_name):
    for e in __encoding_list:
        with open(file_name,"r",encoding=e) as f:
            try:
                f.readline()
            except:
                continue
            return e
    print("Error!!! unknown encoding used in file '{}'".format(file_name))
    exit()

def print_info(info):
    sys.stdout.write(str(info)+"\n")