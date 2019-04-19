import numpy as np
import sys
import os
import json
from utils import *
from progressbar import *
from hmmlearn import hmm
import warnings

class HmmPinyin:
    __eps=1e-12
    def __init__(self,mat_file,maps_file):
        ensure_file_exists(mat_file)
        ensure_file_exists(maps_file)
        
        with open(maps_file,"r") as f:
            maps=json.load(f)
        self.chars=chars=maps["chars"]
        self.char2id=char2id=maps["char2id"]
        self.pinyins=pinyins=maps["pinyins"]
        self.pinyin2id=pinyin2id=maps["pinyin2id"]
        self.pinyin2chars=pinyin2chars=maps["pinyin2chars"]
        self.char2pinyin=char2pinyin=maps["char2pinyin"]
        self.n_chars=n_chars=len(chars)
        self.n_pinyins=n_pinyins=len(pinyins)
        print_info("Maps loaded.");
        
        with open(mat_file,"r") as f:
            mat=json.load(f)
        print_info("Mat loaded.")
        
        startfreq=[mat["startfreq"][c] for c in chars]
        sum_start=sum(startfreq)
        startprob=np.array(list(map(lambda x:float(x)/sum_start,startfreq)))
        emissionprob=np.zeros((n_chars,n_pinyins))
        for i in range(n_chars):
            c=chars[i]
            ps=char2pinyin[c]
            for p in ps:
                emissionprob[i][pinyin2id[p]]=1.0/len(ps)
        print_info("startprob&emissionprob constructed.")
        
        word_freq=mat["words"]
        print_info("Calculating char frequency...")
        char_freq={c:0 for c in chars}
        for word in ProgressBar()(word_freq):
            char_freq[word[0]]+=word_freq[word]
        
        print_info("Construcing transmat...")
        transmat=np.full((n_chars,n_chars),self.__eps)
        for word in ProgressBar()(word_freq):
            c1,c2=word[0],word[1]
            transmat[char2id[c1]][char2id[c2]]=float(word_freq[word])/char_freq[c1]
        for i in range(n_chars):
            if transmat[i].sum()<0.5:
                transmat[i]=np.full((n_chars),1.0/n_chars)
        
        self.model=hmm.MultinomialHMM(n_components,n_chars)
        self.model.startprob_=startprob
        self.model.transmat_=transmat
        self.model.emissionprob_=emissionprob
        print_info("model constructed.")
        
        warnings.filterwarnings("ignore")
        print_info("HmmPinyin constructed!! Have fun!!")
    def predict(self,st):
        arr=st.replace("'"," ").split(" ")
        try:
            pinyin_seq=list(map(lambda p:self.pinyin2id[p],arr))
        except:
            print_info("Error! Invalid pinyin input!")
            return "Invalid input"
        # logprob,res_seq=self.model.decode(np.array([pinyin_seq]).T, algorithm="viterbi")
        res_seq=self.model.predict(np.array([pinyin_seq]).T)
        return ''.join(list(map(lambda id:self.chars[id],res_seq)))
