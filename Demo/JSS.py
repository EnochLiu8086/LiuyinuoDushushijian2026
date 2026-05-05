from LangSC import JSS
g=JSS("json")
Ret=g.Run('SELECT * FROM pinyin WHERE PinYin ="da1"')
print(Ret)
