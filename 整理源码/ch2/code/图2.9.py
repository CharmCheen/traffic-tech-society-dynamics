import pandas as pd
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt

# 读取 Excel 文件
df = pd.read_excel(r"C:\Users\x8615\Desktop\乱七八糟的文件\比赛\大计赛\第三章数据集\图3.9：数据来源中商情报网.xlsx")

# 设置图片清晰度
plt.rcParams['figure.dpi'] = 300

# 设置中文字体（使用黑体）
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 创建一个图形和一组子图，并设置图表大小
fig, ax1 = plt.subplots(figsize=(10, 6))

# 检查数据是否存在 NaN 值，并进行处理
if df['项目数量（个）'].hasnans:
    df['项目数量（个）'] = df['项目数量（个）'].fillna(0)

# 绘制柱状图，设置颜色和标签
bars = ax1.bar(df['年份'], df['项目数量（个）'], color='#1f77b4', label='市场规模（亿元）')

# 设置第一个 y 轴（柱状图）的标签和颜色
ax1.set_xlabel('年份', color='black')
ax1.set_ylabel('项目数量（个）', color='black')
ax1.tick_params(axis='y', labelcolor='black')
ax1.tick_params(axis='x', labelcolor='black')

# 创建第二个 y 轴，共享 x 轴
ax2 = ax1.twinx()

# 绘制折线图，设置颜色和标签
line = ax2.plot(df['年份'], df['项目规模（亿）'], color='#ff7f0e', label='项目规模（亿）', marker='o')

# 修改2024年的坐标轴标签为2024E
years = df['年份'].tolist()
labels = [f'{year}E' if year == 2024 else f'{year}' for year in years]
ax1.set_xticks(years)
ax1.set_xticklabels(labels, color='black')

# 设置第二个 y 轴（折线图）的标签和颜色
ax2.set_ylabel('项目规模（亿）', color='black')
ax2.tick_params(axis='y', labelcolor='black')

# 添加标题
plt.title('2019-2023年中国智慧交通行业千万项目数量及规模统计', color='black')

# 添加图例
lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax2.legend(lines + lines2, labels + labels2, loc='lower right', labelcolor='black')

# 显示图形
plt.show()