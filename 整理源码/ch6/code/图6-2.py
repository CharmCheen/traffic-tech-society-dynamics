import re
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import numpy as np


def extract_information(text):
    regions = ['美国', '欧洲', '中国']
    analysis = {}

    # 提取政策目标差异
    policy_goal_pattern = r'（1）政策目标差异\s*'
    for region in regions:
        pattern = fr'{region}以(.*?)为(目标|核心)，([^。；，]+)(。|；|，)'
        match = re.search(policy_goal_pattern + pattern, text)
        if match:
            if region not in analysis:
                analysis[region] = {}
            analysis[region]['政策目标'] = match.group(3)

    # 提取政策措施差异
    policy_measure_pattern = r'（2）政策措施差异\s*'
    # 资金投入
    for region in regions:
        pattern = fr'在资金投入上{region}(.*?)(。|；|，)'
        match = re.search(policy_measure_pattern + pattern, text)
        if match:
            if region not in analysis:
                analysis[region] = {}
            analysis[region]['资金投入'] = match.group(1)

    # 技术路径
    for region in regions:
        pattern = fr'在技术路径上{region}(.*?)(。|；|，)'
        match = re.search(policy_measure_pattern + pattern, text)
        if match:
            if region not in analysis:
                analysis[region] = {}
            analysis[region]['技术路径'] = match.group(1)

    # 法规框架
    for region in regions:
        pattern = fr'在法规框架上{region}(.*?)(。|；|，)'
        match = re.search(policy_measure_pattern + pattern, text)
        if match:
            if region not in analysis:
                analysis[region] = {}
            analysis[region]['法规框架'] = match.group(1)

    # 提取政策效果差异
    policy_effect_pattern = r'（3）政策效果差异\s*'
    for region in regions:
        pattern = fr'{region}(凭借|通过)(.*?)，([^。；，]+)(。|；|，)'
        match = re.search(policy_effect_pattern + pattern, text)
        if match:
            if region not in analysis:
                analysis[region] = {}
            analysis[region]['政策效果'] = match.group(3)

    return analysis


text = """
（1）政策目标差异
    美国以技术创新为核心，力推自动驾驶商业化，提升交通系统效率，借市场与企业合作，稳固全球交通科技领先地位。欧洲着眼绿色低碳与可持续发展，依托欧盟框架，减少碳排放并推广新能源交通工具，推动区域交通绿色转型 。中国以“交通强国” 为目标，推进基础设施升级与技术融合，通过顶层设计促进区域均衡，致力于构建现代化综合交通体系。
    （2）政策措施差异
    在资金投入上美国靠企业和社会资本，借市场机制推动智能交通技术创新与应用；欧洲利用欧盟基金，为绿色交通发展提供资金；中国以政府投资为主，引导社会资本参与智能交通基础设施建设。在技术路径上，美国侧重单车智能，提升车辆自主性；欧洲关注车路协同与标准化，打造智能化交通体系；中国兼顾车辆和路侧基础设施智能化，通过车路协同优化交通系统。在法规框架上，美国各州自主制定标准，虽利于创新，但阻碍跨州推广；欧洲统一法规，为智能交通发展提供规范保障；中国持续完善法律法规，推动智能交通有序发展。
    （3）政策效果差异
    美国凭借企业强大的创新实力，在技术研发和商业化应用上处于领先地位，能迅速将新技术推向市场。但区域间智能交通发展失衡，部分地区技术应用与基础设施建设滞后，区域发展不平衡程度高。欧洲通过政策引导和资金支持，大力推广新能源交通工具和绿色交通方式，有效降低了交通领域的碳排放，在碳排放控制和绿色交通方面成效显著。不过，其技术落地速度相对较慢，部分先进技术发展受阻，影响了整体发展进度。中国凭借政府的大力支持和集中投入，在交通基础设施建设和智能交通技术规模化应用上优势突出，快速推动交通基础设施升级与行业数字化转型。然而，部分核心技术依赖进口，限制了本土智能交通产业自主发展与国际竞争力提升 。
"""

result = extract_information(text)

# 可视化部分
categories = ['政策目标', '资金投入', '技术路径', '法规框架', '政策效果']
regions = ['美国', '欧洲', '中国']

# 为了更直观展示，这里根据实际内容简单设定一些数值（可根据需求进一步调整）
data_mapping = {
    "美国": {
        "政策目标": 4,
        "资金投入": 3,
        "技术路径": 3,
        "法规框架": 2,
        "政策效果": 3
    },
    "欧洲": {
        "政策目标": 3,
        "资金投入": 3,
        "技术路径": 3,
        "法规框架": 4,
        "政策效果": 3
    },
    "中国": {
        "政策目标": 3,
        "资金投入": 4,
        "技术路径": 4,
        "法规框架": 3,
        "政策效果": 4
    }
}

# 设置中文字体为黑体
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 绘制雷达图
angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
angles += angles[:1]  # 闭合图形

fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(111, polar=True)

for region in regions:
    values = [data_mapping[region][category] for category in categories]
    values += values[:1]  # 闭合图形
    ax.plot(angles, values, linewidth=2, label=region)
    ax.fill(angles, values, alpha=0.2)

# 设置每个数据点的标签
ax.set_thetagrids(np.degrees(angles[:-1]), categories)

# 添加标题
ax.set_title('不同地区自动驾驶政策各方面对比', va='bottom', fontsize=14)

# 添加图例
ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.0))

# 显示表格
table_data = []
for region in regions:
    row = [result[region][category] for category in categories if category in result[region]]
    table_data.append(row)

table = plt.table(cellText=table_data,
                  rowLabels=regions,
                  colLabels=categories,
                  loc='bottom',
                  bbox=[0, -0.6, 1, 0.5])

plt.show()