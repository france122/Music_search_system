import csv
import jieba
from collections import defaultdict
from Jieba_query import cut_for_similarmeasurement
from fuzzywuzzy import process

def search_and_rank_documents_similarity(query_terms):
    with open('../data_files/music.csv', 'r', encoding='gbk') as csvfile_in, \
            open('../data_files/index.csv', 'w', newline='', encoding='gbk') as csvfile_out:
        # 定义CSV文件读取器和写入器
        reader = csv.reader(csvfile_in)
        my_results = []
        #for cut_result in cut_results:
        for row in reader:
            cut_result = row
            best_match = process.extractOne(query_terms, row[1].split("\n"))

            my_results.append([row[0],best_match[0],best_match[1]])
        sorted_results = sorted(my_results, key=lambda x: x[2], reverse=True)
        return sorted_results


def show_results_similarity(query_terms):
    # 执行搜索并排序
    results = search_and_rank_documents_similarity(query_terms)
    search_results = []
    search_results_lyrichighlight = []
    # 迭代结果并以元组形式添加到列表中
    for song_id,lyric_highlight,score in results:
        if score > 45:  # 确保score有效，避免添加无效数据
            search_results.append((song_id,))  # 注意这里变成了单元素元组
            search_results_lyrichighlight.append((song_id,lyric_highlight,score))
    return search_results,search_results_lyrichighlight

#print(inverted_index)
#print(search_and_rank_documents_similarity("翘课 秋千 黄花"))
#(search_results3, results_detail_similarity) = show_results_similarity("小情歌")
#print("*****")
#for i in range(len(search_results3)):
#    print(1)
