import pandas as pd
import matplotlib

matplotlib.use("TkAgg")
import matplotlib.pyplot as plt

# 读取 Excel 文件
df = pd.read_excel(r"C:\Users\x8615\Desktop\乱七八糟的文件\比赛\大计赛\第三章数据集\图2.5：数据来源观知海内信息网.xlsx")

# 设置图片清晰度
plt.rcParams['figure.dpi'] = 300

# 设置中文字体（使用黑体）
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 创建一个图形和一组子图，并设置图表大小
fig, ax1 = plt.subplots(figsize=(10, 6))

# 绘制柱状图，设置颜色和标签
bars = ax1.bar(df['年份'], df['市场规模（亿元）'], color='#1f77b4', label='市场规模（亿元）')

# 设置第一个 y 轴（柱状图）的标签和颜色，将标签颜色改为黑色
ax1.set_xlabel('年份', color='black')
ax1.set_ylabel('市场规模（亿元）', color='black')
ax1.tick_params(axis='y', labelcolor='black')


# 创建第二个 y 轴，共享 x 轴
ax2 = ax1.twinx()

# 绘制折线图，设置颜色和标签
line = ax2.plot(df['年份'], df['增速'], color='#ff7f0e', label='增速（%）', marker='o')

# 修改2024年的坐标轴标签为2024E
years = df['年份'].tolist()
labels = [f'{year}E' if year == 2024 else f'{year}' for year in years]
ax1.set_xticks(years)
ax1.set_xticklabels(labels, color='black')

# 设置第二个 y 轴（折线图）的标签和颜色，将标签颜色改为黑色
ax2.set_ylabel('增速（%）', color='black')
ax2.tick_params(axis='y', labelcolor='black')

# 将两个坐标轴的边框颜色设为黑色
ax1.spines['left'].set_color('black')
ax1.spines['bottom'].set_color('black')
ax2.spines['right'].set_color('black')

# 将两个坐标轴的刻度标签颜色设为黑色
ax1.tick_params(axis='x', colors='black')
ax1.tick_params(axis='y', colors='black')
ax2.tick_params(axis='y', colors='black')

# 添加标题，将标题颜色改为黑色
plt.title('2019 - 2024年E国内高速公路ETC市场规模及预测分析', color='black')

# 添加图例，将图例文本颜色改为黑色
lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
legend = ax2.legend(lines + lines2, labels + labels2, loc='upper right')
for text in legend.get_texts():
    text.set_color('black')

plt.show()