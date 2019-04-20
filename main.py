from src.hmmpinyin import *
import sys
import os
from src.utils import *


ifile=None
ofile=None
def __input():
    if ifile:
        ret=ifile.readline()
    else:
        ret=input()
    return ret.replace('\r','').replace('\n','')

def __output(st):
    if ofile:
        ofile.write(st+'\n')
    else:
        print(st)

if __name__=="__main__":
    if len(sys.argv)>1:
        ifile=sys.argv[1]
        ensure_file_exists(ifile)
        ifile=open(ifile,"r")
    if len(sys.argv)>2:
        ofile=open(sys.argv[2],"w")

    py=HmmPinyin("./data/model/mat.json","./data/model/maps.json")
    st=__input()
    while st:
        __output(py.predict(st))
        st=__input()

    if ifile:
        ifile.close()
    if ofile:
        ofile.close()
