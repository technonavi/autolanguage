
import MeCab
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

# MeCabの初期化
mecab = MeCab.Tagger("-Ochasen")

# 学習データの読み込み
train_df = pd.read_csv("言語学習用データ.csv", encoding='shift_jis')

# 形態素解析を行う関数
def tokenize(text):
    node = mecab.parseToNode(text)
    words = []
    while node:
        if node.surface:
            words.append(node.surface)
        node = node.next
    return ' '.join(words)

# 学習データに形態素解析を適用
train_df["tokenized_text"] = train_df["text"].apply(tokenize)

# 機械学習のパイプラインを設定
pipeline = Pipeline([
    ('vectorizer', TfidfVectorizer()),
    ('classifier', MultinomialNB())
])

# モデルを学習
pipeline.fit(train_df["tokenized_text"], train_df["age_group"])

# テストデータの読み込み
test_df = pd.read_csv("test_data.csv", encoding='shift_jis')

# テストデータに形態素解析を適用
test_df["tokenized_text"] = test_df["text"].apply(tokenize)

# テストデータの年齢層を予測
test_df["predicted_age_group"] = test_df["tokenized_text"].apply(lambda x: pipeline.predict([x])[0])

# 予測結果を出力
print(test_df[["text", "predicted_age_group"]])

# 予測結果をCSVに保存
output_file = "年齢別文章予測結果.csv"
test_df.to_csv(output_file, index=False, encoding='shift_jis', errors='ignore')
print(f"予測結果が {output_file} に保存されました。")
