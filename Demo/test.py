import requests
url = "https://cit.blcu.edu.cn/stree"
sent = '袁隆平常委建议大力实施超级杂交稻“种三产四”丰产工程'
response = requests.post(url, sent).text
print(response)