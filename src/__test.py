from hmmpinyin import *


if __name__=="__main__":
    py=HmmPinyin(model_path="./data/model/")
    print(py.predict("haha"))
    print(py.predict("xi huan chang tiao rap lan qiu"))
    print(py.predict("xihuanchangtiaoraplanqiu"))
    print(py.predict("jiang bian zhao ze yan si cun min"))
    print(py.predict("jiangbianzhaozeyansicunmin"))
    print(py.predict("shanxishengxianshi"))
    print(py.predict("xianzai"))
    print(py.predict("ha ma"))
    print(py.predict("ji ni tai mei"))
