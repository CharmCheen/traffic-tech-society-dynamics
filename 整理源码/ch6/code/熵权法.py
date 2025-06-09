import numpy as np
import pandas as pd

def entropy_weight_method(data):
    normalized_data = data / np.sum(data, axis=0)
    normalized_data = np.where(normalized_data == 0, 1e-10, normalized_data)
    entropy = -np.sum(normalized_data * np.log(normalized_data), axis=0) / np.log(len(data))
    weight = (1 - entropy) / np.sum(1 - entropy)
    return weight

# 读取数据并计算权重
file_path = r"C:\Users\x8615\Desktop\乱七八糟的文件\比赛\大计赛\第三章数据集\指标权重xlsx.xlsx"
df = pd.read_excel(file_path, header=0)
numeric_data = df.select_dtypes(include=np.number).fillna(0)
weights = entropy_weight_method(numeric_data.values)

# 打印结果
print("指标权重：", dict(zip(numeric_data.columns, weights)))
print("权重之和：", np.sum(weights))

# 写入新文件（避免权限问题）
output_path = r"C:\Users\x8615\Desktop\乱七八糟的文件\比赛\大计赛\第三章数据集\熵权法结果.xlsx"
pd.DataFrame({'指标名称': numeric_data.columns, '权重': weights}).to_excel(output_path, index=False)
print(f"结果已保存到：{output_path}")