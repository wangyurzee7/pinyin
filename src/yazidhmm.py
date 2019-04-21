import sys
import os
import json
from .utils import *
from progressbar import *
import math
import numpy as np

class YazidHmm:
    def __init__(self,probemis,grams,startprob,untermedfreq):
        self.__eps=1
        for ele in grams:
            if grams[ele]>0:
                self.__eps=min(self.__eps,1.0/grams[ele])
        self.__eps=math.pow(self.__eps,0.5)
        self.__log_eps=math.log(self.__eps)
        
        for ele in grams:
            grams[ele]=math.log(max(grams[ele],self.__eps))
        for ele in range(len(untermedfreq)):
            untermedfreq[ele]=math.log(max(untermedfreq[ele],1))
        startprob=list(map(lambda x:math.log(max(x,self.__eps)),startprob))
        
        self.probemis=probemis
        self.grams=grams
        self.startprob=startprob
        self.untermedfreq=untermedfreq
    def predict(self,vec):
        n=len(vec)
        if not n:
            return []
        dp=[{} for i in range(n)]
        for e in self.probemis[vec[0]]:
            dp[0][e]={"val":self.startprob[e],"from":-1}
        
        neg_inf=-1e9
        for i in range(1,n):
            for cur_e in self.probemis[vec[i]]:
                now={"val":neg_inf,"from":-1}
                for last_e in self.probemis[vec[i-1]]:
                    tmp=dp[i-1][last_e]["val"]-self.untermedfreq[last_e]
                    if (last_e,cur_e) in self.grams:
                        tmp+=self.grams[(last_e,cur_e)]
                    else:
                        tmp+=self.__log_eps
                    if tmp>now["val"]:
                        now={"val":tmp,"from":last_e}
                dp[i][cur_e]=now
        
        e=-1
        for i in self.probemis[vec[n-1]]:
            if e==-1 or dp[n-1][i]["val"]>dp[n-1][e]["val"]:
                e=i
        ret=[]
        for i in range(n-1,-1,-1):
            if e==-1:
                print_info("Unknown error. Please contact Yazid Wong.")
                return "Unknown error. Please contact Yazid Wong."
            ret.append(e)
            e=dp[i][e]["from"]
        ret.reverse()
        return ret
