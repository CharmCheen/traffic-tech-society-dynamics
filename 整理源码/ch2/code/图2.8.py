import matplotlib

matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import numpy as np

# 设置图片清晰度
plt.rcParams['figure.dpi'] = 300

# 解决中文显示问题
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 数据来源：知网论文《交通强国背景下交通运输行业碳达峰碳中和路径研究》
years = ['2023年', '2025年', '2030年', '2035年', '2040年', '2045年', '2050年', '2055年', '2060年']
road_emission = [10, 11, 12, 13, 9, 7, 4, 2, 1]  # 公路碳排放
civil_aviation_emission = [1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9]  # 民航碳排放
waterway_emission = [1.5, 1.6, 1.7, 1.8, 1.9, 2, 2.1, 2.2, 2.3]  # 水路碳排放
railway_emission = [0.8, 0.9, 1, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6]  # 铁路碳排放
total_emission = [12.99, 13.46, 14.59, 15.46, 12.79, 9.98, 6.48, 3.30, 1.27]  # 碳排放总量

bar_width = 0.2
index = np.arange(len(years))

# 定义不同的颜色
bar_colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']

# 绘制柱状图，取消形状填充
plt.bar(index - 1.5 * bar_width, road_emission, width=bar_width, label='公路碳排放', color=bar_colors[0])
plt.bar(index - 0.5 * bar_width, civil_aviation_emission, width=bar_width, label='民航碳排放', color=bar_colors[1])
plt.bar(index + 0.5 * bar_width, waterway_emission, width=bar_width, label='水路碳排放', color=bar_colors[2])
plt.bar(index + 1.5 * bar_width, railway_emission, width=bar_width, label='铁路碳排放', color=bar_colors[3])

# 绘制折线图
plt.plot(index, total_emission, marker='o', label='碳排放总量', color='orange', linestyle='--')

# 定义垂直和水平偏移量
vertical_offset = 0.5
horizontal_offset = 0.1

# 在折线图上显示数据，调整位置
for i, val in enumerate(total_emission):
    plt.text(index[i] + horizontal_offset, val + vertical_offset, f'{val:.2f}', ha='center', va='bottom', fontsize=8,
             color='orange')

# 设置坐标轴标签和标题
plt.xticks(index, years, rotation=45)
plt.ylabel('交通碳排放总量/亿t')
plt.title('低碳情景下不同交通运输方式碳排放占比图')

# 显示图例
plt.legend()

# 添加数据来源说明
plt.text(0.5, -0.3, "数据来源：知网论文《交通强国背景下交通运输行业碳达峰碳中和路径研究》",
         transform=plt.gca().transAxes, ha='center', fontsize=8, color="grey")

# 调整布局
plt.tight_layout()

# 显示图表
plt.show()
