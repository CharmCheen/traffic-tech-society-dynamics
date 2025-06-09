from wordcloud import WordCloud
import matplotlib

matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import pandas as pd

# 读取Excel文件
file_path = r"C:\Users\x8615\Desktop\乱七八糟的文件\比赛\大计赛\第三章数据集\数据来源职友集.xlsx"  # 替换为你的Excel文件路径
df = pd.read_excel(file_path)

# 提取传统岗位和新兴岗位数据
traditional_jobs = ' '.join(df['传统交通行业岗位'].dropna().tolist())
emerging_jobs = ' '.join(df['新兴岗位'].dropna().tolist())

# 设置Matplotlib字体配置
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号


# 生成词云图的函数
def generate_wordcloud(text, title, font_path):
    wordcloud = WordCloud(
        width=400,  # 设置宽度和高度为相同值
        height=400,
        background_color='white',
        font_path=font_path,  # 指定中文字体路径
        relative_scaling=0.2  # 调整字体大小的均衡程度，值越接近0越均衡
    ).generate(text)

    plt.figure(figsize=(5, 5))  # 设置图形的宽高比为1:1
    plt.imshow(wordcloud)
    plt.axis('off')
    # 取消标题
    # plt.title(title)
    plt.show()


# 定义字体路径
font_path = r"C:/Windows/Fonts/simhei.ttf"

# 生成传统岗位词云图
generate_wordcloud(traditional_jobs, "传统交通行业岗位词云图", font_path)

# 生成新兴岗位词云图
generate_wordcloud(emerging_jobs, "新兴岗位词云图", font_path)
