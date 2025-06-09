import pandas as pd
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

# 手动指定字体文件路径（需要根据实际情况修改）
font_path = r'C:\Windows\Fonts\SimHei.ttf'
font = FontProperties(fname=font_path)

# 读取数据文件
df = pd.read_excel(r"C:\Users\x8615\Desktop\乱七八糟的文件\比赛\大计赛\第三章数据集\图3.2：数据来源中国人民共和国交通运输部及民航局.xlsx")

# 数据清洗与整理
df = df.set_index('年份').sort_index(ascending=False)
columns_to_plot_main = df.columns.drop('民航运输机场')
column_to_plot_secondary = '民航运输机场'

# 创建画布与坐标轴
fig, ax1 = plt.subplots(figsize=(12, 6))

# 绘制主坐标轴柱状图（铁路、内河航道）
width = 0.2
for i, col in enumerate(columns_to_plot_main):
    ax1.bar(df.index + i * width,
            df[col],
            width=width,
            label=col,
            alpha=0.8)

ax1.set_xlabel('年份', fontproperties=font, fontsize=12)
ax1.set_ylabel('里程数（万公里）', fontproperties=font, fontsize=12)
ax1.set_title('2019 - 2024 年交通相关数据对比', fontproperties=font, fontsize=14, pad=20)

# 创建次坐标轴并绘制民航机场折线图
ax2 = ax1.twinx()
ax2.plot(df.index,
         df[column_to_plot_secondary],
         label=column_to_plot_secondary,
         color='#4CAF50',
         marker='o',
         linewidth=2)  # 加粗折线

ax2.set_ylabel('机场数量', fontproperties=font, fontsize=12)

# 合并图例
lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
legend = ax1.legend(lines + lines2, labels + labels2,
                    loc='upper left',
                    bbox_to_anchor=(0.01, 0.98),
                    frameon=False,
                    prop=font)
# 设置图例的 zorder 为一个较大的值，确保在最上层
legend.set_zorder(10)

# 调整坐标轴格式
plt.xticks(df.index + width * (len(columns_to_plot_main) / 2),
           rotation=45,
           fontproperties=font)
ax1.grid(axis='y', linestyle='--', alpha=0.7)

plt.tight_layout()
plt.show()
