"""
作文分词语频统计脚本 - 使用 GPF 分词
"""
import os
from collections import Counter
from LangSC import GPF


def is_valid_word(word):
    """
    判断是否为有效词汇
    - 长度至少2个字符
    - 不包含纯数字、标点符号
    """
    if len(word) < 2:
        return False
    # 排除数字
    if word.isdigit():
        return False
    # 排除纯标点
    if not any('\u4e00' <= c <= '\u9fff' or c.isalpha() for c in word):
        return False
    return True


def read_all_texts(directory):
    """读取目录下所有文本文件"""
    all_text = []
    file_count = 0
    failed_count = 0

    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.endswith('.txt'):
                filepath = os.path.join(root, filename)
                try:
                    # 先尝试 UTF-8
                    with open(filepath, 'r', encoding='utf-8') as f:
                        text = f.read()
                        all_text.append(text)
                        file_count += 1
                except UnicodeDecodeError:
                    # 再尝试 GBK
                    try:
                        with open(filepath, 'r', encoding='gbk') as f:
                            text = f.read()
                            all_text.append(text)
                            file_count += 1
                    except Exception as e:
                        print(f"    读取文件失败 {filepath}: {e}")
                        failed_count += 1

    return all_text, file_count, failed_count


def segment_with_gpf(texts):
    """
    使用 GPF.Segment 对文本进行分词
    """
    gpf = GPF()
    word_counter = Counter()
    total_lines = len(texts)
    processed = 0
    error_count = 0

    for text in texts:
        try:
            # 使用 GPF 的 Segment 方法进行分词
            result = gpf.Segment(text)

            if result:
                # 分词结果用空格分隔
                words = result.split()
                for word in words:
                    if is_valid_word(word):
                        word_counter[word] += 1

        except Exception as e:
            error_count += 1

        processed += 1
        if processed % 50 == 0:
            print(f"    已处理 {processed}/{total_lines} 个文件...")

    if error_count > 0:
        print(f"    警告: {error_count} 个文件处理出错")

    return word_counter


def main():
    # 设置目录路径
    corpus_dir = r'作文'

    print("=" * 60)
    print("作文分词语频统计 (使用 GPF)")
    print("=" * 60)

    # 1. 读取所有文本
    print("\n[1] 读取文本文件...")
    texts, file_count, failed_count = read_all_texts(corpus_dir)
    print(f"    成功读取 {file_count} 个文件")
    if failed_count > 0:
        print(f"    (失败 {failed_count} 个文件)")
    print(f"    总文本长度: {sum(len(t) for t in texts):,} 字符")

    # 2. 使用 GPF 分词
    print("\n[2] 使用 GPF 分词...")
    word_counter = segment_with_gpf(texts)
    print(f"    分词完成，不同词汇数量: {len(word_counter):,}")

    # 3. 排序
    print("\n[3] 按词频排序...")
    sorted_words = word_counter.most_common()

    # 4. 输出结果
    print("\n" + "=" * 60)
    print("词频统计结果 (Top 100)")
    print("=" * 60)
    print(f"{'排名':<6} {'词语':<12} {'词频':<10}")
    print("-" * 30)

    for i, (word, count) in enumerate(sorted_words[:100], 1):
        print(f"{i:<6} {word:<12} {count:<10,}")

    # 5. 保存完整结果
    output_file = 'word_frequency_result.txt'
    print(f"\n[4] 保存完整结果到 {output_file}...")

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("作文分词语频统计结果 (GPF分词)\n")
        f.write("=" * 60 + "\n")
        f.write(f"文件数量: {file_count}\n")
        f.write(f"不同词汇数量: {len(word_counter):,}\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"{'排名':<8} {'词语':<16} {'词频':<12}\n")
        f.write("-" * 40 + "\n")

        for i, (word, count) in enumerate(sorted_words, 1):
            f.write(f"{i:<8} {word:<16} {count:<12,}\n")

    print(f"    已保存 {len(sorted_words):,} 条记录")
    print("\n" + "=" * 60)
    print("处理完成!")
    print("=" * 60)


if __name__ == '__main__':
    main()
