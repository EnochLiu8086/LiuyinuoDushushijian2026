from LangSC import GPF
gpf=GPF()
Txt="中欧班列持续稳定开行，夯实了亚欧大陆互联互通的基础"
js=gpf.Parse(Txt,Structure="Dep")
gpf.ShowStructure(js)
