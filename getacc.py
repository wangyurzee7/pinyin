import os
import sys
import json
from src.utils import *

if __name__=='__main__':
    if len(sys.argv)<3:
        sys.stdout.write("Too Few Arguments.\n")
        exit()
    with open(sys.argv[1],"r",encoding=get_encoding(sys.argv[1])) as f:
        r1=f.readlines()
    with open(sys.argv[2],"r",encoding=get_encoding(sys.argv[2])) as f:
        r2=f.readlines()
    if len(r1)!=len(r2):
        sys.stdout.write("Line number does not match!!")
    n=len(r1)
    res_s=(0,0)
    res_c=(0,0)
    for i in range(n):
        s1,s2=r1[i],r2[i]
        s1=s1.replace('\r','').replace('\n','').replace(' ','')
        s2=s2.replace('\r','').replace('\n','').replace(' ','')
        res_s=(res_s[0]+1,res_s[1]+int(s1==s2))
        if len(s1)==len(s2):
            m=len(s1)
            for j in range(m):
                c1,c2=s1[j],s2[j]
                res_c=(res_c[0]+1,res_c[1]+int(c1==c2))
    buf="acc of sentences = {}/{} = {}%".format(res_s[1],res_s[0],10000*res_s[1]/res_s[0]/100.0)
    buf+=" ;  acc of chars = {}/{} = {}%".format(res_c[1],res_c[0],10000*res_c[1]/res_c[0]/100.0)
    print(buf)
