from hmmpinyin import *


if __name__=="__main__":
    py=HmmPinyin("../data/model/mat.json","../data/model/maps.json")
    print(py.predict("jiang bian zhao ze yan si cun min"))
    print(py.predict("shan xi sheng xi an shi"))
    print(py.predict("xian zai ji dian le"))
    print(py.predict("ha ma"))
