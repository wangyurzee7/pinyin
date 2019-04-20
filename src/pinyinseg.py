import sys
import os
import json
from utils import *
from progressbar import *
import math
import numpy as np

class PinyinSeg:
    def __init__(self,pinyins,grams,startprob):
        merged_freq={i+j:0 for i in pinyins for j in pinyins}
        for ele in grams:
            merged_freq[ele[0]+ele[1]]+=grams[ele]
        self.__eps=1
        for ele in merged_freq:
            if merged_freq[ele]>0:
                self.__eps=min(self.__eps,1.0/merged_freq[ele])
        self.__eps=math.pow(self.__eps,1.5)
        self.__log_eps=math.log(self.__eps)
        self.__half_log_eps=self.__log_eps/2
        
        for ele in grams:
            grams[ele]=math.log(max(grams[ele],self.__eps))
        for ele in merged_freq:
            merged_freq[ele]=math.log(max(merged_freq[ele],self.__eps))
        for ele in startprob:
            startprob[ele]=math.log(max(startprob[ele],self.__eps))
        max_len=0
        for p in pinyins:
            max_len=max(max_len,len(p))
        
        self.max_len=max_len
        self.pinyins=pinyins
        self.grams=grams
        self.startprob=startprob
        self.merged_freq=merged_freq
    def segment(self,st):
        seq=st.replace("'"," ").split(' ')
        most_left=[0]
        cur_left=0
        for p in seq:
            for i in p:
                most_left.append(cur_left)
            cur_left+=len(p)
        st="".join(seq)
        n=len(st)
        dp=np.full((n+1,self.max_len+1),self.__log_eps*(n+1))
        last_k=np.full((n+1,self.max_len+1),1)
        dp[0][0]=0
        
        for i in range(1,n+1):
            for k in range(1,self.max_len+1):
                if i-k<most_left[i]:
                    break
                cur_p=st[i-k:i]
                for l in range(0,self.max_len+1):
                    if i-k-l<most_left[i-k]:
                        break
                    last_p=st[i-k-l:i-k]
                    tmp=dp[i-k][l]
                    if not cur_p in self.pinyins:
                        tmp+=self.__log_eps*2
                        # print("log_eps*2={}".format(self.__log_eps*2))
                    elif l==0 or not last_p in self.pinyins:
                        tmp+=self.startprob[cur_p]
                    else:
                        tmp+=self.grams[(last_p,cur_p)]
                        cur_found=cur_p in self.merged_freq
                        last_found=last_p in self.merged_freq
                        if cur_found and last_found:
                            dlt=self.merged_freq[cur_p]
                        elif cur_found:
                            dlt=(self.merged_freq[last_p+cur_p]+self.merged_freq[cur_p])/2
                        elif last_found:
                            dlt=0
                        else:
                            dlt=self.merged_freq[last_p+cur_p]
                        # print(dlt)
                        tmp-=dlt
                    if tmp>dp[i][k]:
                        dp[i][k]=tmp
                        last_k[i][k]=l;
                # print("dp[{}][{}]={}".format(i,k,dp[i][k]))
        k=0
        for i in range(1,self.max_len+1):
            if dp[n][i]>dp[n][k]:
                k=i
        ret=[]
        while n>0:
            if k>0:
                ret.append(st[n-k:n])
            n,k=n-k,last_k[n][k]
        ret.reverse()
        # print(ret)
        return ret
