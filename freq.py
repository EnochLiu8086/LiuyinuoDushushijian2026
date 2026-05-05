"""
词频统计脚本：分句、分词、统计前100高频词
分词引擎：LangSC GPF（优先）→ jieba（备选）
编码：GBK/GB18030 自动检测
"""

import os
import re
import json
import ast
from collections import Counter

try:
    from LangSC import GPF as _GPF
    _gpf = _GPF()
except ImportError:
    _gpf = None

try:
    import jieba
    HAS_JIEBA = True
except ImportError:
    HAS_JIEBA = False


# =============================================================================
# 编码与文件读取
# =============================================================================

def load_text_file(file_path):
    """读取文本文件，自动检测编码（优先 GBK）"""
    with open(file_path, 'rb') as f:
        raw = f.read(4)
    if raw.startswith(b'\xef\xbb\xbf'):
        enc = 'utf-8-sig'
    elif raw.startswith(b'\xfe\xff'):
        enc = 'utf-16-be'
    elif raw.startswith(b'\xff\xfe'):
        enc = 'utf-16-le'
    else:
        enc = 'gbk'
    for try_enc in [enc, 'gb18030', 'gbk', 'utf-8', 'latin1']:
        try:
            with open(file_path, 'r', encoding=try_enc) as f:
                return f.read()
        except Exception:
            continue
    return ""


# =============================================================================
# 分句
# =============================================================================

def split_sentences(text):
    """按句末标点分句"""
    parts = re.split(r'(?<=[。！？；])', text)
    return [p.strip() for p in parts if p.strip()]


# =============================================================================
# 分词引擎 1：本地 GPF
# =============================================================================

def _segment_gpf(text, max_len=512):
    """
    使用本地 LangSC GPF 分词。
    GPF 在当前环境下直接返回正确解码的 UTF-8 JSON 字符串，
    格式如 '["今天/t", "的/u", "天气/n"]'。
    """
    if _gpf is None:
        return None

    all_words = []
    for start in range(0, len(text), max_len):
        chunk = text[start:start + max_len]
        try:
            raw_result = _gpf.Parse(chunk)
            # GPF 直接返回 UTF-8 JSON 字符串，直接解析
            parsed = ast.literal_eval(raw_result)
            for item in parsed:
                if '/' not in item:
                    continue
                word_part, pos_part = item.split('/', 1)
                pos = pos_part.strip()
                if pos in ('w', 'x'):
                    continue
                word = word_part.strip()
                if word:
                    all_words.append(word)
        except Exception:
            return None
    return all_words


# =============================================================================
# 分词引擎 2：jieba（离线备选）
# =============================================================================

def _segment_jieba(text):
    """jieba 分词（完全本地，无网络依赖）"""
    words = []
    for sent in split_sentences(text):
        for w in jieba.cut(sent):
            w = w.strip()
            if w:
                words.append(w)
    return words


# =============================================================================
# 分词入口（引擎调度）
# =============================================================================

def segment(text):
    """
    中文分词入口，按优先级调用：
      1. 本地 GPF（最快，结果准）
      2. jieba（兜底，完全离线）
    返回词列表，如 ["今天", "天气", "真", "好"]
    """
    words = _segment_gpf(text)
    if words is not None and len(words) > 0:
        return words
    if HAS_JIEBA:
        return _segment_jieba(text)
    return []


# =============================================================================
# 停用词
# =============================================================================

STOP_WORDS = {
    '的', '了', '是', '在', '我', '有', '和', '就', '不', '人', '都',
    '一', '这', '个', '上', '也', '很', '到', '说', '要', '去', '你',
    '会', '着', '看', '好', '还', '他', '她', '它', '们', '把', '被',
    '给', '向', '从', '对', '又', '再', '才', '之', '而', '且', '所',
    '以', '因', '为', '于', '中', '大', '小', '多', '少', '几', '些',
    '最', '更', '太', '真', '那', '哪', '谁', '吗', '呢', '吧', '啊',
    '自己', '别人', '大家', '一起', '一直', '一样', '一下', '一点',
    '一个', '一种', '没有', '就是', '只是', '还是', '已经', '正在', '现在',
    '什么', '怎么', '这样', '那样', '怎么', '这些', '那些', '可以', '不能',
    '如果', '因为', '所以', '但是', '而且', '或者', '然后', '其实', '然后',
}


# =============================================================================
# 核心函数
# =============================================================================

def File2Sent(F, Sent):
    """读取文件内容并分句，结果存入 Sent 列表"""
    text = load_text_file(F)
    if not text:
        return
    sents = split_sentences(text)
    Sent.extend(sents)


def Add2Freq_F(R, Freq_F):
    """将分词结果 R（词列表）累加到 Freq_F 词频字典"""
    for w in R:
        if not Freq_F.get(w):
            Freq_F[w] = 0
        Freq_F[w] += 1


def GetFreq_F(F, Freq_F):
    """统计单个文件的词频"""
    Sent = []
    File2Sent(F, Sent)
    for S in Sent:
        R = segment(S)
        Add2Freq_F(R, Freq_F)


def MergeF2Ret(Freq_F, Ret):
    """将单文件词频 Freq_F 合并到全局 Ret"""
    for k, v in Freq_F.items():
        if not Ret.get(k):
            Ret[k] = 0
        Ret[k] += v


def GetFileList(Dir, FileList):
    """递归获取目录下所有 .txt 文件"""
    if not os.path.isdir(Dir):
        return
    for entry in os.listdir(Dir):
        path = os.path.join(Dir, entry)
        if os.path.isdir(path):
            GetFileList(path, FileList)
        elif path.endswith('.txt'):
            FileList.append(path)


def GetOneFileFreq(F, Ret):
    """统计单个文件的词频并合并到 Ret"""
    Freq_F = {}
    GetFreq_F(F, Freq_F)
    MergeF2Ret(Freq_F, Ret)


def GetFreq(Dir):
    """统计目录下所有文件的词频，返回全局词频字典"""
    FileList = []
    Ret = {}
    GetFileList(Dir, FileList)
    for i, F in enumerate(FileList, 1):
        GetOneFileFreq(F, Ret)
        print(f"[{i}/{len(FileList)}] {F}")
    return Ret


# =============================================================================
# 输出
# =============================================================================

def Output(Ret, top_n=100):
    """输出 Top N 高频词"""
    filtered = {w: c for w, c in Ret.items()
                if w not in STOP_WORDS and len(w) >= 2}
    sorted_items = sorted(filtered.items(), key=lambda x: x[1], reverse=True)
    print(f"\n{'='*50}")
    print(f"  前 {top_n} 高频词")
    print(f"{'='*50}")
    print(f"  {'排名':<6}{'词语':<15}{'频次':<8}")
    print(f"  {'-'*29}")
    for i, (w, c) in enumerate(sorted_items[:top_n], 1):
        print(f"  {i:<6}{w:<15}{c:<8}")
    print(f"{'='*50}")
    return sorted_items[:top_n]


# =============================================================================
# 主程序
# =============================================================================

if __name__ == '__main__':
    base = os.path.dirname(os.path.abspath(__file__))
    Dir = os.path.join(base, "作文")

    print(f"开始词频统计，目录: {Dir}")
    print(f"GPF 可用: {_gpf is not None}  |  jieba 可用: {HAS_JIEBA}")
    print(f"{'='*50}\n")

    Ret = GetFreq(Dir)
    top100 = Output(Ret, top_n=100)

    out_json = os.path.join(base, "freq_result_top100.json")
    with open(out_json, 'w', encoding='utf-8') as f:
        json.dump([[w, c] for w, c in top100], f, ensure_ascii=False, indent=2)
    print(f"\n结果已保存: {out_json}")
