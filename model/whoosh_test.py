from whoosh.index import create_in
from whoosh.fields import *
from whoosh.index import open_dir
from whoosh.qparser import QueryParser
from whoosh.query import *
import csv
import jieba
from jieba.analyse import ChineseAnalyzer
from collections import defaultdict
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # 这里保险的就是直接先把绝对路径加入到搜索路径
sys.path.insert(0, os.path.join(BASE_DIR))
sys.path.insert(0, os.path.join(BASE_DIR, 'data'))  # 把data所在的绝对路径加入到了搜索路径，这样也可以直接访问dataset.csv文件了

# 这句代码进行切换目录
os.chdir(BASE_DIR)   # 把目录切换到当前项目，这句话是关键
#print(os.getcwd())
def whoosh_index():
    analyzer = ChineseAnalyzer()
    # 构建索引
    if not os.path.exists("../indexdir"):
        os.mkdir("../indexdir")
    schema = Schema(songID=TEXT(stored=True), lyrics=TEXT(stored=True, analyzer=analyzer))
    ix = create_in("indexdir", schema)
    writer = ix.writer()

    # 读取CSV文件并存入文档
    with open('data_files/music.csv', 'r', encoding='gbk') as csvfile_in:
        # 定义CSV文件读取器和写入器
        reader = csv.reader(csvfile_in)
        # 跳过标题行（如果存在）
        next(reader, None)
        # 遍历CSV文件的每一行
        for row in reader:
            writer.add_document(songID=row[0], lyrics=row[1])
    writer.commit()

def whoosh_search(keywords):
    # 搜索
    results = []
    ix = open_dir("../indexdir")
    searcher = ix.searcher()
    parser = QueryParser("lyrics", schema=ix.schema)
    for keyword in keywords:
        q = parser.parse(keyword)
        result = searcher.search(q)
        for hit in result :
            results.append(hit["songID"])

    return results


