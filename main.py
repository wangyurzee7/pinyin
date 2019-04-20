from src.hmmpinyin import *
import sys
import os
from src.utils import *


ifile=None
ofile=None
of2=None
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
        of2=open(sys.argv[2]+'.segres',"w")

    py=HmmPinyin(model_path="./src/data/model/")
    st=__input()
    while st:
        __output(py.predict(st))
        if of2:
            of2.write(py.predict(st.replace(' ',''))+'\n')
        st=__input()

    if ifile:
        ifile.close()
    if ofile:
        ofile.close()
    if of2:
        of2.close()
