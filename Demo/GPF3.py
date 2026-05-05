from LangSC import GPF
import json
Line= """
{"Words": ["瑞士", "率先", "破门", "，", "沙其理", "梅开二度", "。"], 
"Tags": ["ns", "d", "v", "w", "nr", "i", "w"], 
"Relations": [{"U1": 2, "U2":0,"R":"A0","KV":"KV1"},
{"U1": 2, "U2":1,"R":"Mod","KV":"KV2"},
{"U1": 5, "U2":4,"R":"A0","KV":"KV3"}]} """

S=json.loads(Line)
Txt="".join(S["Words"])
gpf=GPF()
gpf.SetText(Txt)
ColNo=0
Units=[]
for i in range(len(S["Words"])):
    UnitNo=gpf.AddUnit(S["Words"][i],ColNo+len(S["Words"][i])-1)
    Units.append(UnitNo)
    gpf.AddUnitKV(UnitNo,"POS",S["Tags"][i])
    ColNo=+len(S["Words"][i])
    
for R in S["Relations"]:
    gpf.AddRelation(Units[R["U1"]],Units[R["U2"]],R["R"])

gpf.ShowRelation("r.png")
    


