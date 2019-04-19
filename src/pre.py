# usage: python3 pre.py [char_file] [map_file] [doc_list] [result_path='./'] [ignore_threshold=0]

import sys
import os
import json
import numpy as np

def ensure_file_exists(file_name):
    if (not os.path.exists(file_name)) or (not os.path.isfile(file_name)):
        print("File '{}' not found!".format(file_name))
        exit()

def ensure_dir_exists(dir_path):
    if (not os.path.exists(dir_path)) or os.path.isfile(dir_path):
        print("Dir '{}' not found!".format(dir_path))
        exit()

__capital='aeiou'
def starts_with_capital(st):
    for c in __capital:
        if st.startswith(c):
            return True
    return False

def read_chars(file_name):
    with open(file_name,"r",encoding="gbk") as f:
        lst=list(''.join(f.readlines()))
        return lst,{c:id for id,c in enumerate(lst)}

def read_pinyins(file_name):
    with open(file_name,"r",encoding="gbk") as f:
        lst=[]
        pinyin2chars={}
        char2pinyin={}
        for line in f.readlines():
            arr=line.replace('\n','').replace('\r','').split(' ')
            pinyin,char_list=arr[0],arr[1:]
            lst.append(pinyin)
            pinyin2chars[pinyin]=char_list
            for char in char_list:
                if char in char2pinyin:
                    char2pinyin[char].append(pinyin)
                else:
                    char2pinyin[char]=[pinyin]
        return lst,{p:id for id,p in enumerate(lst)},pinyin2chars,char2pinyin

def get_sentences(content):
    content+='#'
    sentences=[]
    cur_s=""
    last_c=None
    for c in content:
        if c in chars:
            cur_s+=c
            last_c=c
        elif last_c:
            last_c=None
            sentences.append(cur_s)
            cur_s=""
    return sentences

def work(list_file,chars,char2id,pinyins,pinyin2id,pinyin2chars,char2pinyin):
    with open(list_file,"r") as f:
        char_cnt=len(chars)
        pinyin_cnt=len(pinyins)
        ret={}
        ret["words"]={}
        ret["pinyins"]={}
        ret["startfreq"]={c:0 for c in chars}
        file_list=f.readlines()
        for file in file_list:
            file=file.replace('\r','').replace('\n','')
            ensure_file_exists(file)
            with open(file,"r") as f:
                print(" - Treating file '{}'".format(file))
                for line in f.readlines():
                    try:
                        content=json.loads(line)["html"]
                    except:
                        continue
                    sentences=get_sentences(content)
                    # solve with ret
                    for s in sentences:
                        for i in range(len(s)-1):
                            word=s[i:i+2]
                            if not word in ret["words"]:
                                ret["words"][word]=0
                            ret["words"][word]+=1
                        cur=[[]]
                        ret["startfreq"][s[0]]+=1
                        # TODO: something with ret["pinyins"]
        return ret

if __name__=='__main__':
    if (len(sys.argv)<4):
        print("Too Few Arguments.")
        exit()
    char_file=sys.argv[1]
    map_file=sys.argv[2]
    doc_list=sys.argv[3]
    try:
        res_path=sys.argv[4]
    except:
        print("Result path not read. Set to './' by default.")
        res_path='./'
    try:
        ignore_t=float(sys.argv[5])
    except:
        print("Ignore threshold not read(or not a float). Set to 0 by default.")
        ignore_t=0
    ensure_file_exists(char_file)
    ensure_file_exists(map_file)
    ensure_file_exists(doc_list)
    ensure_dir_exists(res_path)
    
    chars,char2id=read_chars(char_file)
    print("Char list read. [ Count of char = {} ]".format(len(chars)))
    
    pinyins,pinyin2id,pinyin2chars,char2pinyin=read_pinyins(map_file)
    print("Pinyin map read. [ Count of pinyin = {} ]".format(len(pinyins)))
    
    if len(chars)!=len(char2pinyin):
        print("Num of char in pinyin table and dict does not match")
    
    prepare_res=work(doc_list,chars,char2id,pinyins,pinyin2id,pinyin2chars,char2pinyin)
    tw="中国" # test word
    print("All docs read. [ Test: count of word '{}' is {} ]".format(tw,prepare_res["words"][tw]))
    
    # dump_result(res_path,prepare_res,ignore_t)