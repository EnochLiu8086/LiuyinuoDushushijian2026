from LangSC import BCC
g=BCC("largecorpus")
Ret=g.Run("喜欢",Command="Context",Number=100)
print(Ret)
