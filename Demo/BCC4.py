from LangSC import BCC
Query='''
OriOn()
Speedup(1)
Condition("$1=$2")
Handle1=GetAS("|v_一","一","","","","","0,1","","","")
Handle0=GetAS("一_v|","一","","","","","","1,0","","")
Handle2=JoinAS(Handle1,Handle0,"ShareQuery")
Handle3=Freq(Handle2,"$Q","0",100)
Ret=Output(Handle3,100)
return Ret
'''
gpf=BCC("corpus")
JS=gpf.Run(Query)
print(JS)
