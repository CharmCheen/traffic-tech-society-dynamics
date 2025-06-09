import pandas as pd
import matplotlib

matplotlib.use("TkAgg")
import matplotlib.pyplot as plt

# 读取第一个文件
excel_file_2018 = pd.ExcelFile(r"C:\Users\x8615\Desktop\乱七八糟的文件\比赛\大计赛\第三章数据集\图2.14 2018.xlsx")

# 获取所有表名
sheet_names_2018 = excel_file_2018.sheet_names

# 解析出 2018 年的数据
df_2018 = excel_file_2018.parse(sheet_names_2018[0])

# 读取第二个文件
excel_file_2024 = pd.ExcelFile(r"C:\Users\x8615\Desktop\乱七八糟的文件\比赛\大计赛\第三章数据集\图2.14：数据来源百度地图与高德地图.xlsx")

# 获取所有表名
sheet_names_2024 = excel_file_2024.sheet_names

# 获取对应工作表数据
df_2024 = excel_file_2024.parse('Sheet1')

# 合并 2018 年和 2024 年的数据
merged_df = pd.merge(df_2018, df_2024, on='城市')

# 设置图片清晰度
plt.rcParams['figure.dpi'] = 300

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 设置画布大小
plt.figure(figsize=(14, 8))

# 绘制高峰行程延时指数对比柱状图
bar_width = 0.35
index = range(len(merged_df['城市']))
plt.bar(index, merged_df['2018年高峰行程延时指数'], bar_width, label='2018年高峰行程延时指数')
plt.bar([i + bar_width for i in index], merged_df['2024年高峰行程延时指数'], bar_width, label='2024年高峰行程延时指数')
plt.xlabel('城市')
plt.ylabel('高峰行程延时指数')
plt.title('不同城市 2018 年和 2024 年高峰行程延时指数对比')
plt.xticks([i + bar_width / 2 for i in index], merged_df['城市'])

# 将图例移动到图表下方
plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), fancybox=True, shadow=True, ncol=2)

# 展示图片
plt.show()

# 绘制高峰平均车速对比柱状图
plt.figure(figsize=(14, 8))
plt.bar(index, merged_df['2018年高峰平均车速(km/h)'], bar_width, label='2018年高峰平均车速(km/h)')
plt.bar([i + bar_width for i in index], merged_df['2024年高峰平均车速(km/h)'], bar_width, label='2024年高峰平均车速(km/h)')
plt.xlabel('城市')
plt.ylabel('高峰平均车速(km/h)')
plt.title('不同城市 2018 年和 2024 年高峰平均车速对比')
plt.xticks([i + bar_width / 2 for i in index], merged_df['城市'])

# 将图例移动到图表下方
plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1), fancybox=True, shadow=True, ncol=2)

# 展示图片
plt.show()
