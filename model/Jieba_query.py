import csv
import jieba
from collections import defaultdict

# 读取CSV文件并建立倒排索引
with open('data_files/music.csv', 'r', encoding='gbk') as csvfile_in, \
        open('data_files/index.csv', 'w', newline='', encoding='utf-8') as csvfile_out:
    # 定义CSV文件读取器和写入器
    reader = csv.reader(csvfile_in)
    writer = csv.writer(csvfile_out)

    # 跳过标题行（如果存在）
    next(reader, None)

    # 倒排索引字典，键是词，值是该词出现的歌曲编号及其频率
    inverted_index = defaultdict(lambda: defaultdict(int))

    # 遍历CSV文件的每一行
    for row in reader:
        song_id = row[0]  # 歌曲编号
        lyrics = row[1]  # 歌曲歌词

        # 使用jieba进行分词
        seg_list = jieba.lcut_for_search(lyrics)
        # 遍历分词结果，建立倒排索引并计数
        for word in seg_list:
            if len(word) > 1:  # 过滤掉单个字符的词（可选）
                inverted_index[word][song_id] += 1
'''
                # 将倒排索引写入新的CSV文件
    # 写入标题行
    writer.writerow(['Word', 'Song IDs and Frequencies'])

    # 遍历倒排索引并写入CSV文件
    for word, song_info in inverted_index.items():
        # 格式化歌曲编号和频率，以字符串形式存储
        song_ids_with_freq = ', '.join(f'{song_id}:{freq}' for song_id, freq in song_info.items())
        # 写入当前词及其关联的歌曲编号和频率
        writer.writerow([word, song_ids_with_freq])

print("Inverted index has been saved to index.csv")
'''
from collections import defaultdict
import math
# 假设的文档总数
N = 1331  # 有1331个文档
# 计算IDF
def calculate_idf(inverted_index, N):
    idf = {}
    for term, postings in inverted_index.items():
        df = len(postings)  # 文档频率
        idf[term] = math.log(N / df) if df else 0  # 避免除数为0
    return idf


# 计算给定查询词项在给定文档中的TF-IDF值
def calculate_tf_idf_for_document(query_terms, idf, inverted_index, song_id):
    tf_idf_scores = {}
    for term in query_terms:
        if term in inverted_index and song_id in inverted_index[term]:
            tf = inverted_index[term][song_id]  # 假设词频已经给出
            tf_idf_scores[term] = tf * idf[term]
    return tf_idf_scores


# 计算查询在所有文档中的TF-IDF值，并返回按TF-IDF值排序的文档列表
def search_and_rank_documents(query_terms, inverted_index, N):
    idf = calculate_idf(inverted_index, N)
    document_scores = {}

    # 遍历所有文档，计算TF-IDF值
    for song_id in set().union(*[list(postings.keys()) for postings in inverted_index.values()]):
        tf_idf_scores = calculate_tf_idf_for_document(query_terms, idf, inverted_index, song_id)
        # 假设我们简单地将所有词项的TF-IDF值相加作为文档的总分
        document_scores[song_id] = sum(tf_idf_scores.values()) if tf_idf_scores else 0

        # 按TF-IDF值对文档进行排序
    sorted_documents = sorted(document_scores.items(), key=lambda x: x[1], reverse=True)
    return sorted_documents


def show_results(query_terms,inverted_index):
    # 执行搜索并排序
    results = search_and_rank_documents(query_terms, inverted_index, 1331)
    search_results=[]
    # 打印结果
    for song_id, score in results:
            if score:
                search_results.append(song_id)
    return search_results

    # 基于TF-IDF值排序和返回结果（在这个例子中，我们只有一个文档，但如果有多个，你可以根据TF-IDF值进行排序）