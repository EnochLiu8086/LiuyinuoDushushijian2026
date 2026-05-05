"""
作文文本处理：分句、分段、词频统计
分词引擎：LangSC GPF web 服务（chunk API）
"""

import os
import re
import json
import requests
from collections import Counter


# =============================================================================
# 编码与文件读取
# =============================================================================

def load_text_file(file_path):
    """读取文本文件，自动检测编码"""
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
        except:
            continue
    return ""


# =============================================================================
# 分句与分段
# =============================================================================

def split_sentences(text):
    """按句末标点分句"""
    parts = re.split(r'(?<=[。！？；])', text)
    return [p.strip() for p in parts if p.strip()]


def split_paragraphs(text):
    """按空行分段"""
    blocks = re.split(r'\n\s*\n', text)
    return [b.strip() for b in blocks if b.strip()]


# =============================================================================
# 分词：LangSC GPF web 服务（chunk API）
# =============================================================================

CHUNK_API = 'https://cit.blcu.edu.cn/chunk/'


def segment(text, timeout=60):
    """
    使用 LangSC GPF chunk API 分词
    复现: gpf.Parse(text, Structure="Chunk") 的效果
    返回词列表，如 ["今天", "天气", "真", "好"]
    """
    words = []
    for sent in split_sentences(text):
        sent = sent.strip()
        if not sent:
            continue
        try:
            r = requests.post(CHUNK_API, sent.encode('utf-8'), timeout=timeout)
            if r.status_code == 200:
                data = json.loads(r.content)
                units = data.get('Units', [])
                pos_list = data.get('POS', [])
                for i, u in enumerate(units):
                    pos = pos_list[i] if i < len(pos_list) else ''
                    if pos != 'w' and u.strip():  # w = 标点
                        words.append(u.strip())
        except Exception:
            pass
    return words


# =============================================================================
# 词频统计
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
}


def count_freq(words, top_n=50):
    """词频统计，去除停用词"""
    filtered = [w for w in words if w not in STOP_WORDS and len(w) >= 2]
    return Counter(filtered).most_common(top_n)


# =============================================================================
# 主程序
# =============================================================================

def main():
    base = os.path.dirname(os.path.abspath(__file__))
    folder = os.path.join(base, "作文")
    out_json = os.path.join(base, "essay_analysis_result.json")

    files = sorted([f for f in os.listdir(folder) if f.endswith('.txt')])
    print(f"文件总数: {len(files)}\n")

    all_words = []
    results = {}
    skipped = []

    for i, fname in enumerate(files, 1):
        fpath = os.path.join(folder, fname)
        text = load_text_file(fpath)

        if not text:
            skipped.append(fname)
            print(f"[{i}/{len(files)}] [跳过] {fname}")
            continue

        paras = split_paragraphs(text)
        sents = [s for p in paras for s in split_sentences(p)]
        words = segment(text)
        freq = count_freq(words)

        results[fname] = {
            'paragraph_count': len(paras),
            'sentence_count': len(sents),
            'word_count': len(words),
            'top_words': freq,
            'paragraphs': paras,
            'sentences': sents,
        }

        all_words.extend(words)
        print(f"[{i}/{len(files)}] {fname}  段:{len(paras)} 句:{len(sents)} 词:{len(words)}")

    # 全局词频
    total_freq = count_freq(all_words)
    total_para = sum(r['paragraph_count'] for r in results.values())
    total_sent = sum(r['sentence_count'] for r in results.values())
    total_words = sum(r['word_count'] for r in results.values())

    # 打印报告
    print(f"\n{'='*60}")
    print(f"  作文分析报告")
    print(f"{'='*60}")
    print(f"  文件总数: {len(files)}")
    if skipped:
        print(f"  跳过文件: {skipped}")
    print(f"  段落总数: {total_para}")
    print(f"  句子总数: {total_sent}")
    print(f"  词数总数: {total_words}")

    print(f"\n【全局词频 Top 50】")
    print(f"  {'排名':<6}{'词语':<15}{'频次':<8}")
    print(f"  {'-'*29}")
    for i, (w, c) in enumerate(total_freq, 1):
        print(f"  {i:<6}{w:<15}{c:<8}")

    sorted_files = sorted(results.items(), key=lambda x: x[1]['word_count'], reverse=True)
    print(f"\n{'='*60}")
    print(f"  各文件词频（前15，按词数排序）")
    print(f"{'='*60}")
    for fname, info in sorted_files[:15]:
        print(f"\n【{fname.replace('.txt', '')}】")
        print(f"  段落:{info['paragraph_count']} 句子:{info['sentence_count']} 词数:{info['word_count']}")
        if info['top_words']:
            print(f"  " + "  ".join(f"{w}({c})" for w, c in info['top_words'][:10]))

    # 保存 JSON
    out_data = {
        'total_files': len(files),
        'skipped_files': skipped,
        'total_paragraphs': total_para,
        'total_sentences': total_sent,
        'total_words': total_words,
        'total_word_freq': [[w, c] for w, c in total_freq],
        'file_results': {
            fname: {
                'paragraph_count': r['paragraph_count'],
                'sentence_count': r['sentence_count'],
                'word_count': r['word_count'],
                'top_words': [[w, c] for w, c in r['top_words']],
                'paragraphs': r['paragraphs'],
                'sentences': r['sentences'],
            }
            for fname, r in results.items()
        }
    }
    with open(out_json, 'w', encoding='utf-8') as f:
        json.dump(out_data, f, ensure_ascii=False, indent=2)
    print(f"\n[结果已保存] {out_json}")


if __name__ == '__main__':
    main()
