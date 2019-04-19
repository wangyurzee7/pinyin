# usage: python3 pre.py [char_file] [map_file] [doc_list] [result_path='./'] [ignore_threshold=0]
import sys
import os
import json
from utils import *
from progressbar import *

def read_chars(file_name):
    with open(file_name,"r",encoding=get_encoding(file_name)) as f:
        lst=list(''.join(f.readlines()))
        return lst,{c:id for id,c in enumerate(lst)}

def read_pinyins(file_name):
    with open(file_name,"r",encoding=get_encoding(file_name)) as f:
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

def work(list_file,chars,char2id,pinyins,pinyin2id,pinyin2chars,char2pinyin,threshold):
    with open(list_file,"r",encoding=get_encoding(list_file)) as f:
        char_cnt=len(chars)
        pinyin_cnt=len(pinyins)
        ret={}
        ret["words"]={}
        ret["pinyins"]={}
        ret["startfreq"]={c:0 for c in chars}
        for file_name in f.readlines():
            file_name=file_name.replace('\r','').replace('\n','')
            ensure_file_exists(file_name)
            with open(file_name,"r",encoding=get_encoding(file_name)) as f:
                print_info(" - Treating file '{}'".format(file_name))
                lines=f.readlines()
                bar=ProgressBar()
                for i in bar(range(len(lines))):
                    try:
                        content=json.loads(lines[i])["html"]
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
                        ret["startfreq"][s[0]]+=1
                        # TODO: something with ret["pinyins"]
        _cnt={}
        words=[]
        for word in ret["words"]:
            cur_freq=ret["words"][word]
            for p1 in char2pinyin[word[0]]:
                for p2 in char2pinyin[word[1]]:
                    if not (p1,p2) in _cnt:
                        _cnt[(p1,p2)]=0
                    _cnt[(p1,p2)]+=cur_freq
            words.append(word)
        for word in words:
            cur_freq=ret["words"][word]
            valid=False
            for p1 in char2pinyin[word[0]]:
                for p2 in char2pinyin[word[1]]:
                    valid=valid or cur_freq>=_cnt[(p1,p2)]*threshold
            if not valid:
                ret["words"].pop(word)
        return ret
    

if __name__=='__main__':
    if (len(sys.argv)<4):
        print_info("Too Few Arguments.")
        exit()
    char_file=sys.argv[1]
    map_file=sys.argv[2]
    doc_list=sys.argv[3]
    try:
        res_path=sys.argv[4]
    except:
        print_info("Result path not read. Set to './' by default.")
        res_path='./'
    try:
        ignore_t=float(sys.argv[5])
    except:
        print_info("Ignore threshold not read(or not a float). Set to 0 by default.")
        ignore_t=0
    ensure_file_exists(char_file)
    ensure_file_exists(map_file)
    ensure_file_exists(doc_list)
    ensure_dir_exists(res_path)
    
    chars,char2id=read_chars(char_file)
    print_info("Char list read. [ Count of char = {} ]".format(len(chars)))
    
    pinyins,pinyin2id,pinyin2chars,char2pinyin=read_pinyins(map_file)
    print_info("Pinyin map read. [ Count of pinyin = {} ]".format(len(pinyins)))
    
    if len(chars)!=len(char2pinyin):
        print_info("Num of char in pinyin table and dict does not match")
    
    prepare_res=work(doc_list,chars,char2id,pinyins,pinyin2id,pinyin2chars,char2pinyin,ignore_t)
    tw="中国" # test word
    print_info("All docs read. [ Test: count of word '{}' is {} ]".format(tw,prepare_res["words"][tw]))
    
    maps={}
    maps["chars"]=chars
    maps["char2id"]=char2id
    maps["pinyins"]=pinyins
    maps["pinyin2id"]=pinyin2id
    maps["pinyin2chars"]=pinyin2chars
    maps["char2pinyin"]=char2pinyin
    
    with open(res_path+"/mat.json","w") as f:
        json.dump(prepare_res,f)
    with open(res_path+"/maps.json","w") as f:
        json.dump(maps,f)
    print_info("Dumped.")