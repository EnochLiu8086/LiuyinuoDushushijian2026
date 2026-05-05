import requests
Txt="中欧班列持续稳定开行，夯实了亚欧大陆互联互通的基础"
url = 'https://cit.blcu.edu.cn/stree'
r = requests.post(url=url, data=Txt)
r.encoding = 'utf8'
print(r.text)