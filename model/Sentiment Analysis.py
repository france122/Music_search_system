from collections import defaultdict
import os
import re
import jieba
import codecs
import pandas as pd
import csv

# 生成stopword表，需要去除一些否定词和程度词汇
stopwords = set()
fr = open('C:/Users/lenovo/Desktop/Music_search_system/data_files/stopwords.txt', 'r', encoding='utf-8')
for word in fr:
    stopwords.add(word.strip())  # Python strip() 方法用于移除字符串头尾指定的字符（默认为空格或换行符）或字符序列。
# 读取否定词文件
not_word_file = open('C:/Users/lenovo/Desktop/Music_search_system/data_files/否定词.txt', 'r+', encoding='utf-8')
not_word_list = not_word_file.readlines()
not_word_list = [w.strip() for w in not_word_list]
# 读取程度副词文件
degree_file = open('C:/Users/lenovo/Desktop/Music_search_system/data_files/程度副词.txt', 'r+',encoding='utf-8')
degree_list = degree_file.readlines()
degree_list = [item.split(',')[0] for item in degree_list]
# 生成新的停用词表
with open('C:/Users/lenovo/Desktop/Music_search_system/data_files/new_stopwords.txt', 'w', encoding='utf-8') as f:
    for word in stopwords:
        if (word not in not_word_list) and (word not in degree_list):
            f.write(word + '\n')


# jieba分词后去除停用词
def seg_word(sentence):
    seg_list = jieba.cut(sentence)
    seg_result = []
    for i in seg_list:
        seg_result.append(i)
    stopwords = set()
    with open('C:/Users/lenovo/Desktop/Music_search_system/data_files/new_stopwords.txt', 'r+',encoding='utf-8') as fr:
        for i in fr:
            stopwords.add(i.strip())
    words = jieba.lcut(sentence, cut_all=False)

    return list(filter(lambda word: word not in stopwords, seg_result))


# 找出文本中的情感词、否定词和程度副词
def classify_words(word_list):
    # 读取情感词典文件
    sen_file = open('C:/Users/lenovo/Desktop/Music_search_system/data_files/BosonNLP_sentiment_score.txt', 'r+', encoding='utf-8')
    # 获取词典文件内容
    sen_list = sen_file.readlines()
    # 创建情感字典
    sen_dict = defaultdict()
    # 读取词典每一行的内容，将其转换成字典对象，key为情感词，value为其对应的权重
    for i in sen_list:
        if len(i.split(' ')) == 2:
            sen_dict[i.split(' ')[0]] = i.split(' ')[1]

    # 读取否定词文件
    not_word_file = open('C:/Users/lenovo/Desktop/Music_search_system/data_files/否定词.txt', 'r+', encoding='utf-8')
    not_word_list = not_word_file.readlines()
    # 读取程度副词文件
    degree_file = open('C:/Users/lenovo/Desktop/Music_search_system/data_files/程度副词.txt', 'r+',encoding='utf-8')
    degree_list = degree_file.readlines()
    #degree_dict = defaultdict()
    #for i in degree_list:
    #    degree_dict[i.split(',')[0]] = i.split(',')[1]

    sen_word = dict()
    not_word = dict()
    degree_word = dict()
    # 分类
    for i in range(len(word_list)):
        word = word_list[i]
        if word in sen_dict.keys() and word not in not_word_list and word not in degree_list:
            # 找出分词结果中在情感字典中的词
            sen_word[i] = sen_dict[word]
        elif word in not_word_list and word not in degree_list:
            # 分词结果中在否定词列表中的词
            not_word[i] = -1
        elif word in degree_list:
            # 分词结果中在程度副词中的词
            degree_word[i] = degree_list[word]

    # 关闭打开的文件
    sen_file.close()
    not_word_file.close()
    degree_file.close()
    # 返回分类结果
    return sen_word, not_word, degree_word


# 计算情感词的分数
def score_sentiment(sen_word, not_word, degree_word, seg_result):
    # 权重初始化为1
    W = 1
    score = 0
    # 情感词下标初始化
    sentiment_index = -1
    # 情感词的位置下标集合
    sentiment_index_list = list(sen_word.keys())
    # 遍历分词结果
    for i in range(0, len(seg_result)):
        # 如果是情感词
        if i in sen_word.keys():
            # 权重*情感词得分
            score += W * float(sen_word[i])
            # 情感词下标加一，获取下一个情感词的位置
            sentiment_index += 1
            if sentiment_index < len(sentiment_index_list) - 1:
                # 判断当前的情感词与下一个情感词之间是否有程度副词或否定词
                for j in range(sentiment_index_list[sentiment_index], sentiment_index_list[sentiment_index + 1]):
                    # 更新权重，如果有否定词，权重取反
                    if j in not_word.keys():
                        W *= -1
                    elif j in degree_word.keys():
                        W *= float(degree_word[j])
        # 定位到下一个情感词
        if sentiment_index < len(sentiment_index_list) - 1:
            i = sentiment_index_list[sentiment_index + 1]
    return score


# 计算得分
def sentiment_score(sentence):
    # 1.对文档分词
    seg_list = seg_word(sentence)
    # 2.将分词结果转换成字典，找出情感词、否定词和程度副词
    sen_word, not_word, degree_word = classify_words(seg_list)
    # 3.计算得分
    score = score_sentiment(sen_word, not_word, degree_word, seg_list)
    return score


df = pd.read_csv('C:/Users/lenovo/Desktop/Music_search_system/data_files/music.csv', encoding='gb18030',dtype={'Lyrics': str},index_col='SongID').astype(str)  # 确保编码与你的CSV文件一致
with open('C:/Users/lenovo/Desktop/Music_search_system/data_files/sentiment_score.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(["SongID", "score"])
    for i in range(0,df.size):
        score = sentiment_score(df['Lyrics'][i])
        print(df.index[i],score)
        writer.writerow([df.index[i],score])
