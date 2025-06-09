import pandas as pd
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

# 手动指定字体文件路径（需要根据实际情况修改）
font_path = r'C:\Windows\Fonts\SimHei.ttf'
font = FontProperties(fname=font_path)

# 模拟数据读取（根据实际文件路径修改）
df = pd.read_excel(r"C:\Users\x8615\Desktop\乱七八糟的文件\比赛\大计赛\第三章数据集\图3.1.xlsx", sheet_name="Sheet1")

# 数据清洗
df = df.rename(columns={'A': '年份'})  # 假设年份列在A列
df = df.set_index('年份').sort_index(ascending=False)  # 按年份升序排列
columns_to_plot = df.columns.drop('等级公路里程比重(%)')  # 需要柱状图展示的列

# 创建画布与坐标轴
fig, ax1 = plt.subplots(figsize=(12, 6))

# 绘制柱状图（主坐标轴）
width = 0.6  # 柱状图宽度
for i, col in enumerate(columns_to_plot):
    ax1.bar(df.index + i*width/len(columns_to_plot),
            df[col],
            width=width/len(columns_to_plot),
            label=col,
            alpha=0.8)

ax1.set_xlabel('年份', fontproperties=font, fontsize=12)
ax1.set_ylabel('公路里程（万公里）', fontproperties=font, fontsize=12)
ax1.set_title('中国公路发展情况（2005-2023）', fontproperties=font, fontsize=14, pad=20)

# 创建次坐标轴（折线图）
ax2 = ax1.twinx()
line = ax2.plot(df.index, df['等级公路里程比重(%)'],
                marker='o',
                color='red',
                linewidth=2,
                markersize=8,
                label='等级公路里程比重(%)')
ax2.set_ylabel('比重（%）', fontproperties=font, fontsize=12)
ax2.set_ylim(40, 100)  # 固定比例尺范围

# 合并图例
lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines + lines2, labels + labels2,
           loc='upper left',
           bbox_to_anchor=(0.01, 0.98),
           frameon=False, prop=font)

# 调整坐标轴格式
plt.xticks(df.index, rotation=45, fontproperties=font)
ax1.grid(axis='y', linestyle='--', alpha=0.7)

# 显示图表
plt.tight_layout()
plt.show()