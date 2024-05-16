#!/user/bin/env python3
# -*- coding: utf-8 -*-
import time
from model.Jieba_query import inverted_index
import model
from model.whoosh_test import whoosh_search,whoosh_index

keywords = input().split()  # 将传来的关键词赋给keywords
start_time1 = time.time()
search_results1 = model.Jieba_query.show_results(keywords, inverted_index)
end_time1 = time.time()# 在表里查询符合条件的条目赋给key_words
time1 = round(end_time1 - start_time1, 3)
print("1.基于TF-IDF检索，检索时间：", time1, "s")
print("检索结果", search_results1)

start_time2 = time.time()
whoosh_index()
search_results2 = whoosh_search(keywords)
end_time2 = time.time()
time2 = round(end_time2 - start_time2, 3)
print("2.基于whoosh检索，检索时间：", time2, "s")
print("检索结果", search_results2)


