import pandas as pd
import matplotlib

matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter

# 读取 Excel 文件
df = pd.read_excel(r"C:\Users\x8615\Desktop\乱七八糟的文件\比赛\大计赛\第三章数据集\图3.4数据来源：国家统计局.xlsx")

# 设置图片清晰度
plt.rcParams['figure.dpi'] = 300
# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']

# 提取绘图数据
years = df['年份']
columns_to_plot = ['货运量总计', '铁路', '公路', '水路', '海洋', '民航', '管道']

# 创建画布
plt.figure(figsize=(12, 8))

# 绘制各运输方式货运量的折线图
for column in columns_to_plot:
    plt.plot(years, df[column], label=column, marker='o')

# 设置图表标题和坐标轴标签
plt.title('不同运输方式货运量随年份变化趋势')
plt.xticks(rotation=45)
plt.ylabel('货运量（万吨）')

# 设置图例，放置在图表下方，并缩小图例大小
plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=len(columns_to_plot), prop={'size': 6})

# 显示网格线
plt.grid(True)

# 禁用科学计数法
ax = plt.gca()
ax.yaxis.set_major_formatter(ScalarFormatter(useOffset=False, useMathText=False))
ax.yaxis.get_major_formatter().set_scientific(False)

# 显示图表
plt.tight_layout()
plt.show()