
library(qgraph)    
library(readxl)     
library(Matrix)    


data_path <- "E:/计算机设计大赛/数据增强后的影响路径数据.xlsx"  
data <- read_excel(data_path)
# 假设数据列依次为：MS, TP, IG, IGR, EI, CM, SS, AS, AM, AQ, CE, RU, AC, PC, RHS
colnames(data) <- c("date","MS", "TP", "IG", "IGR", "EI", "CM", "SS", "AS", "AM", "AQ", "CE", "RU", "AC", "PC", "RHS")
data_scaled <- as.data.frame(scale(data[-1]))

# 3. 计算相关矩阵并转换为正定矩阵
S <- cor(data_scaled)
S_pd <- as.matrix(nearPD(S)$mat)

# 4. 估计偏相关网络
network <- EBICglasso(S_pd, n = nrow(data_scaled), gamma = 0.5, threshold = TRUE)

all_nodes <- colnames(data_scaled)
node_colors <- rep("gray80", length(all_nodes))
names(node_colors) <- all_nodes

# 分组配色：
# "MS", "TP" 使用 #00a9c7 配色
node_colors[c("MS", "TP")] <- "#00a9c7"
# "IG", "IGR", "EI" 使用 #00c4bd 配色
node_colors[c("IG", "IGR", "EI")] <- "#00c4bd"
# "CM", "SS", "AS", "AM" 使用 #48dba3 配色
node_colors[c("CM", "SS", "AS", "AM")] <- "#48dba3"
# "AQ", "CE", "RU" 使用 #a4ed84 配色
node_colors[c("AQ", "CE", "RU")] <- "#a4ed84"
# "AC", "PC", "RHS" 使用 #f9f871 配色
node_colors[c("AC", "PC", "RHS")] <- "#f9f871"

# 6. 绘制网络图，同时在边上标注偏相关系数，去掉图例
qgraph(network,
       layout = "spring",                   # 弹簧布局，确保节点均衡分布
       labels = all_nodes,                  # 节点标签
       label.cex = 1.2,                     # 标签字号
       vsize = 12,                          # 节点大小
       edge.color = "#8765b2",              # 连接线颜色使用 #008bbd
       directed = FALSE,                    # 无向网络
       curve = 0.3,                         # 边曲率参数，减少重叠
       mar = c(5,5,5,5),                    # 图形边距
       title = "Partial Correlation Network",
       title.cex = 1.5,
       color = node_colors,                 # 节点颜色设置
       legend = FALSE,                      # 去掉图例
       whatLabels = round(network, 2),      # 在边上显示偏相关系数，保留两位小数
       edge.label.cex = 1.2)                # 边标签字号
cat("Influence Path (Partial Correlation) Matrix:\n")
print(round(network, 2))
centrality_results <- centrality(network)
print(centrality_results)
library(igraph)
centrality_results <- centrality(network)

