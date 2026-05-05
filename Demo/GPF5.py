from LangSC import GPF
gpf=GPF()
Text="我们大家很辛苦"
gpf.SetText(Text)
JS='["我们","大家","很","辛苦"]'
gpf.AddStructure(JS)
JS='["我们","大家","很辛苦"]'
gpf.AddStructure(JS)
gpf.ShowGrid()
Grid=gpf.GetGrid()
for Col in Grid:
    for Unit in Col:
        print(Unit,gpf.GetUnitKV(Unit,"Word"))