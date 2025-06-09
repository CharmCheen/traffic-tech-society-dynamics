import pandas as pd
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt

# 读取 Excel 文件
excel_file = pd.ExcelFile(r"C:\Users\x8615\Desktop\乱七八糟的文件\比赛\大计赛\第三章数据集\图3.3：数据来源国家统计局.xlsx")

# 获取对应工作表中数据
df = excel_file.parse('Sheet1')

# 设置图片清晰度
plt.rcParams['figure.dpi'] = 300

# 设置中文字体（使用黑体）
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 绘制不同年份下不同出行方式旅客周转量的折线图
plt.figure(figsize=(12, 6))
plt.plot(df['年份'], df['铁路'], label='铁路', marker='o')
plt.plot(df['年份'], df['公路'], label='公路', marker='s')
plt.plot(df['年份'], df['水路'], label='水路', marker='^')
plt.plot(df['年份'], df['民航'], label='民航', marker='v')

# 设置标题和标签
plt.title('不同年份不同出行方式旅客周转量折线图')
plt.xticks(rotation=45)
# 添加 y 轴单位
plt.ylabel('旅客周转量（亿人公里）')

# 显示图例，放在最下面
columns_to_plot = ['铁路', '公路', '水路', '民航']
plt.legend(loc='lower center', bbox_to_anchor=(0.5, -0.25), ncol=len(columns_to_plot), prop={'size': 6})

# 显示图表
plt.tight_layout()
plt.show()