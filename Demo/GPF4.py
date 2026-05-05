from LangSC import GPF
gpf=GPF()

Text="饭孩子们都吃完了"
Text="饭孩子们都吃光了"

Text="孩子们都吃撑了"
gpf.SetText(Text)
Child=gpf.AddUnit("孩子们",2)
All=gpf.AddUnit("都",3)
Eat=gpf.AddUnit("吃",4)
Full=gpf.AddUnit("撑了",6)

gpf.AddUnitKV(Eat,"POS","V")
gpf.AddUnitKV(Full,"POS","V")

gpf.AddRelation(Eat,All,"mod")
gpf.AddRelation(Eat,Full,"mod")
gpf.AddRelation(Eat,Child,"sbj")
gpf.AddRelation(Full,Child,"sbj")
gpf.AddRelationKV(Full,Child,"sbj","K1","V1")
gpf.AddRelationKV(Full,Child,"sbj","K2","V2")
R=gpf.GetRelation()

for r in R:
    print(r)
    print(gpf.GetUnitKV(r[0],"Word"),gpf.GetUnitKV(r[1],"Word"),r[2])
    KVs=gpf.GetRelationKV(r[0],r[1],r[2])
    for K,Vs in KVs.items():
        print(K)
