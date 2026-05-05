import json
from LangSC import GPF

# 创建GPF实例
gpf = GPF()

# 分析句子
text = "年轻的工程师认真地设计新产品"

# 获取分词与词性（Parse返回JSON字符串，需用json.loads解析）
Ret = gpf.Parse(text, Structure="POS")
result = json.loads(Ret)

print("分词与词性：")
for tag in result:
    print(f"  {tag}", end="")  # tag已是"word/pos"格式
print()

# 获取依存关系（返回Web服务JSON，可直接可视化）
Ret = gpf.Parse(text, Structure="Dep")

print("\n依存关系：")
gpf.ShowStructure(Ret, "依存结构.png")
print(Ret)  # 打印原始JSON查看

# 获取树形结构
Ret = gpf.Parse(text, Structure="Tree")
tree = json.loads(Ret)

print("\n树形结构：")
print(json.dumps(tree, ensure_ascii=False, indent=2))