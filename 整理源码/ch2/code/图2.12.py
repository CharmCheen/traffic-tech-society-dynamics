import pandas as pd
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

# 读取 Excel 文件
excel_file = pd.ExcelFile(r"C:\Users\x8615\Desktop\乱七八糟的文件\比赛\大计赛\第三章数据集\图2-13出行方式变革数据来源交通运输行业发展统计公报.xlsx")

# 获取指定工作表中的数据
df = excel_file.parse('Sheet1')

# 设置图片清晰度
plt.rcParams['figure.dpi'] = 300

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 统一减小字体大小
plt.rcParams.update({'font.size': 6})

# 定义一组颜色循环，用于饼图
colors = list(mcolors.TABLEAU_COLORS.values())

# 创建一个 2x2 的子图布局
fig, axes = plt.subplots(2, 2, figsize=(10, 10))

# 遍历每一年的数据
for i, (index, row) in enumerate(df.iterrows()):
    year = int(row['年份'])  # 将年份转换为整数，去除小数点
    modes = df.columns[1:]
    values = row[modes]

    # 计算子图的位置
    row_idx = i // 2
    col_idx = i % 2
    wedges = axes[row_idx, col_idx].pie(values, autopct='%1.1f%%', textprops={'fontsize': 6}, colors=colors, radius=1)[0]
    # 缩小标题字体大小，这里设为 10，你可以根据需要调整
    axes[row_idx, col_idx].set_title(f'{year} 年各出行方式占比', fontweight='bold', fontsize=10)
    # 设置子图背景颜色为淡灰色
    axes[row_idx, col_idx].set_facecolor('#f9f9f9')

# 获取所有类别名称
modes = df.columns[1:]

# 设置全局图例
fig.legend(
    wedges, modes,
    loc='lower center',
    fontsize=6,
    ncol=len(modes),
    frameon=True,  # 显示图例边框
    facecolor='white',  # 图例背景颜色为白色
    edgecolor='gray',  # 图例边框颜色为灰色
    labelspacing=1.0  # 图例项之间的垂直间距
)

# 调整子图之间的间距
plt.subplots_adjust(wspace=0.3, hspace=0.3)

# 显示图表
plt.show()