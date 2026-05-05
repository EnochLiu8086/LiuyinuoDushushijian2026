from LangSC import BCC
import json
g = BCC("Corpus")
Ret = g.Run("喜欢{}", Command="Freq", Number=20)
print(json.loads(Ret)["Freq"].items())

