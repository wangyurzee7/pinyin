import numpy as np
import sys
import os
import json
from .utils import *
from progressbar import *
import warnings

class HmmPinyin:
    __eps=1e-12
    def __init__(self,model_path="data/model/",mat_file=None,maps_file=None,predictor="yazidhmm"):
        if not mat_file:
            mat_file=model_path+"/mat.json"
        if not maps_file:
            maps_file=model_path+"/maps.json"
        ensure_file_exists(mat_file)
        ensure_file_exists(maps_file)
        self.predictor=predictor
        
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
        word_freq=mat["words"]
        print_info("Mat loaded.")
        
        # predictor initialization
        if predictor=="hmmlearn":
            from hmmlearn import hmm
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
            
            self.model=hmm.MultinomialHMM(n_components=n_chars)
            self.model.startprob_=startprob
            self.model.transmat_=transmat
            self.model.emissionprob_=emissionprob
            print_info("model constructed.")
            
            warnings.filterwarnings("ignore")
        elif predictor=="yazidhmm":
            from .yazidhmm import YazidHmm
            pid2cids=[list(map(lambda c:char2id[c],pinyin2chars[pinyins[pid]])) for pid in range(n_pinyins)]
            idmat={(char2id[w[0]],char2id[w[1]]):word_freq[w] for w in ProgressBar()(word_freq)}
            idstartprob=[mat["startfreq"][chars[cid]] for cid in range(n_chars)]
            self.model=YazidHmm(pid2cids,idmat,idstartprob)
            print_info("model constructed.")
        else:
            print_info("No predictor called {}.".format(predictor))
            exit()
        
        # segmentor initialization
        from .pinyinseg import PinyinSeg
        pinyin_grams={(i,j):0 for i in pinyins for j in pinyins}
        for word in ProgressBar()(word_freq):
            for p1 in char2pinyin[word[0]]:
                for p2 in char2pinyin[word[1]]:
                    pinyin_grams[(p1,p2)]+=word_freq[word]
        
        pinyin_startprob={i:0 for i in pinyins}
        for p in pinyins:
            for c in pinyin2chars[p]:
                pinyin_startprob[p]+=mat["startfreq"][c]
        self.segmentor=PinyinSeg(pinyins=pinyins,grams=pinyin_grams,startprob=pinyin_startprob)
        print_info("Segmentor constructed.")
        
        print_info("HmmPinyin constructed!! Have fun!!")
    def predict_valid_seq(self,seq):
        if not seq:
            return ""
        if self.predictor=="hmmlearn":
            seq=np.array([seq]).T
        res_seq=self.model.predict(seq)
        return ''.join(list(map(lambda id:self.chars[id],res_seq)))
    def predict(self,st,need_segmentation=False):
        seged=False
        if need_segmentation or st.find(" ")==-1:
            arr=self.segmentor.segment(st)
            seged=True
        else:
            arr=st.replace("'"," ").split(" ")
        
        seq=[]
        ret=""
        for p in arr:
            if p in self.pinyins:
                seq.append(self.pinyin2id[p])
            else:
                if not seged:
                    return self.predict(st,need_segmentation=True)
                ret+=self.predict_valid_seq(seq)+p
                seq=[]
        ret+=self.predict_valid_seq(seq)
        return ret
