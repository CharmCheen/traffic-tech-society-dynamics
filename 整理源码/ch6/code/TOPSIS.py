import numpy as np
import matplotlib

matplotlib.use("TkAgg")
import matplotlib.pyplot as plt

# 设置图片清晰度
plt.rcParams['figure.dpi'] = 300

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False


def topsis(data, weights, benefit_type):
    # 数据标准化
    normalized_data = np.zeros_like(data)
    for j in range(data.shape[1]):
        if benefit_type[j]:  # 效益型指标
            normalized_data[:, j] = data[:, j] / np.sqrt(np.sum(data[:, j] ** 2))
        else:  # 成本型指标
            normalized_data[:, j] = (np.max(data[:, j]) - data[:, j]) / np.sqrt(
                np.sum((np.max(data[:, j]) - data[:, j]) ** 2))

    # 计算加权标准化矩阵
    weighted_normalized_data = normalized_data * weights

    # 确定正理想解和负理想解
    positive_ideal_solution = np.array(
        [np.max(weighted_normalized_data[:, j]) if benefit_type[j] else np.min(weighted_normalized_data[:, j]) for j in
         range(data.shape[1])])
    negative_ideal_solution = np.array(
        [np.min(weighted_normalized_data[:, j]) if benefit_type[j] else np.max(weighted_normalized_data[:, j]) for j in
         range(data.shape[1])])

    # 计算各方案到正理想解和负理想解的距离
    distances_to_positive = np.sqrt(np.sum((weighted_normalized_data - positive_ideal_solution) ** 2, axis=1))
    distances_to_negative = np.sqrt(np.sum((weighted_normalized_data - negative_ideal_solution) ** 2, axis=1))

    # 计算贴近度
    closeness_coefficients = distances_to_negative / (distances_to_positive + distances_to_negative)

    return closeness_coefficients


# 从Excel文件中提取的数据
data = np.array([
    [0.82, 0.78, 2000000.0, 0.12, 120.0, 15000.0, 0.0035, 25.0, 85.0, 0.22, 0.08, 0.78],  # 中国
    [0.75, 0.65, 1500000.0, 0.18, 80.0, 12000.0, 0.004, 18.0, 80.0, 0.18, 0.12, 0.72],  # 美国
    [0.78, 0.7, 1800000.0, 0.15, 95.0, 10000.0, 0.0038, 22.0, 88.0, 0.25, 0.07, 0.82]  # 欧洲
])

# 从Excel文件中提取的权重
weights = np.array([
    0.00664051294586974, 0.0280770066995007, 0.0680176848252486, 0.13328423644708,
    0.138412176390814, 0.136906902581793, 0.0148495841105716, 0.0880091102004363,
    0.00763302480716648, 0.0880091102004363, 0.276071337510147, 0.0140893132809354
])

# 定义指标类型，True表示效益型指标（越大越好），False表示成本型指标（越小越好）
benefit_type = [True, True, True, True, True, True, True, True, True, True, False, True]

# 计算贴近度
closeness_coefficients = topsis(data, weights, benefit_type)

# 输出每个国家的贴近度
countries = ["中国", "美国", "欧洲"]
for i, coefficient in enumerate(closeness_coefficients):
    print(f"{countries[i]}的贴近度: {coefficient:.4f}")

# 根据贴近度排序
sorted_indices = np.argsort(closeness_coefficients)[::-1]
sorted_countries = [countries[i] for i in sorted_indices]
sorted_coefficients = [closeness_coefficients[i] for i in sorted_indices]

print("排序结果（从优到劣）:")
for country in sorted_countries:
    print(country)

# 可视化结果
plt.figure(figsize=(10, 6), facecolor='#f4f4f4')
bars = plt.bar(sorted_countries, sorted_coefficients, color=['#FF5575', '#FFD36A', '#6299FF'])
plt.xlabel("国家/地区", fontsize=12, fontweight='bold')
plt.ylabel("贴近度", fontsize=12, fontweight='bold')
plt.title("中美欧智能交通成熟度评价结果", fontsize=16, fontweight='bold')
plt.ylim(0, 1)  # 设置y轴范围

# 添加数据标签
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2, height + 0.01, f'{height:.4f}', ha='center', va='bottom', fontsize=10)

# 添加图例
legend_labels = [f'{country}: {coeff:.4f}' for country, coeff in zip(sorted_countries, sorted_coefficients)]
plt.legend(bars, legend_labels, loc='upper right', fontsize=10)

plt.tight_layout()
plt.show()
