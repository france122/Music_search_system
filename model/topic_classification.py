import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import defaultdict
import jieba

# 读取停用词文件，每行一个停用词
def load_stopwords(stopwords_file):
    with open(stopwords_file, 'r', encoding='utf-8') as f:
        return set(line.strip() for line in f if line.strip())

    # 加载停用词
stopwords = load_stopwords('../data_files/stopwords.txt')  # 停用词文件名为stopwords.txt

# 加载CSV文件
df = pd.read_csv('../data_files/music.csv', encoding='gbk',dtype={'Lyrics': str},index_col='SongID').astype(str)  # 确保编码与你的CSV文件一致


# 预处理函数：分词并去除停用词
def preprocess_lyrics(lyrics):
    words = jieba.lcut(lyrics,cut_all=False)
    filtered_words = [word for word in words if word not in stopwords]
    return ' '.join(filtered_words)


# 对每首歌的歌词进行预处理
preprocessed_lyrics = df['Lyrics'].apply(preprocess_lyrics)

# 初始化TF-IDF向量化器
vectorizer = TfidfVectorizer()

# 拟合并转换预处理后的歌词为TF-IDF矩阵
tfidf_matrix = vectorizer.fit_transform(preprocessed_lyrics)

# 获取特征名（即分词后的单词）
feature_names = vectorizer.get_feature_names_out()

# 找出每首歌TF-IDF最高的三个词
top_terms_per_song = defaultdict(list)
for idx, row in enumerate(tfidf_matrix.toarray()):
    # 获取当前索引对应的SongID（因为我们设置了SongID为DataFrame的索引）
    song_id = df.index[idx]
    # 排序并取前三个最高TF-IDF的词
    top_indices = row.argsort()[::-1][:3]
    for index in top_indices:
        top_terms_per_song[song_id].append((feature_names[index], row[index]))

    # 打印结果
for song_id, terms in top_terms_per_song.items():
    print(f"Song ID: {song_id}, Top 3 TF-IDF terms are:")
    for term, tfidf in terms:
        print(f"    {term}: {tfidf:.4f}")
    print()