import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import gensim
from collections import defaultdict
import jieba
from topic_classification import tfidf_matrix,vectorizer,df

# 使用LDA模型
n_topics = 3  # 假设你想要识别5个主题
lda_model = LatentDirichletAllocation(n_components=n_topics,
                                      random_state=0)
lda_output = lda_model.fit_transform(tfidf_matrix)


# lda_output现在包含了每首歌在每个主题上的概率分布

# 打印每首歌的主题分类
def print_topic_classification(lda_output, n_topics):
    for idx, doc_topics in enumerate(lda_output):
        song_id = df.index[idx]
        print(f"Song ID: {song_id}")
        topic_idx = doc_topics.argmax()  # 获取概率最高的主题索引
        print(f"Main topic: {topic_idx}")
        # 如果你还想打印其他主题的概率，可以这样做：
        for topic_idx, prob in enumerate(doc_topics):
            print(f"Topic {topic_idx}: {prob:.2f}")
        print()
print_topic_classification(lda_output, n_topics)


# 如果你还想获取每个主题的关键词，可以使用之前的print_top_words函数
def print_top_words(model, feature_names, n_top_words):
    for topic_idx, topic in enumerate(model.components_):
        message = "Topic #%d: " % topic_idx
        message += " ".join([feature_names[i]
                             for i in topic.argsort()[:-n_top_words - 1:-1]])
        print(message)

print_top_words(lda_model, vectorizer.get_feature_names_out(), 10)