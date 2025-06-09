import pandas as pd
from wordcloud import WordCloud, STOPWORDS
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt

# 读取 CSV 文件
df = pd.read_csv('data.csv')  # 替换为你的文件路径

# 数据预处理（根据实际情况调整）
text = '\n'.join(df['职位'].dropna().astype(str))  # 替换为你的文本列名

# 生成词云
wordcloud = WordCloud(
    width=800,
    height=600,
    background_color='white',
    stopwords=STOPWORDS,
    max_words=200,
    font_path='simhei.ttf'  # 中文需要指定字体文件
).generate(text)

# 显示词云
plt.figure(figsize=(12, 8))
plt.imshow(wordcloud)
plt.axis('off')
plt.show()

# 保存词云图片
wordcloud.to_file('wordcloud.png')