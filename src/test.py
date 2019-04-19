from hmmpinyin import *


if __name__=="__main__":
    py=HmmPinyin("./mat.json","./maps.json")
    print(py.predict("jiang bian zhao ze yan si cun min"))
