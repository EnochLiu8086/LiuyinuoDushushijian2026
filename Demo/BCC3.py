from LangSC import BCC
gpf=BCC("corpus")
JS=gpf.Run("(v)一(v){$1=$2}",Print="Lua")
print(JS)
