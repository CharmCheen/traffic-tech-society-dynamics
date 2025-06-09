
library(readxl)    
library(ggplot2)   
library(qgraph)    

# 2. 读取数据
data_path <- "E:/计算机设计大赛/数据增强后的影响路径数据.xlsx"
data <- read_excel(data_path)

# 3. 修改变量名称为英文缩写
# 假设 Excel 中变量的顺序为：
# "新能源汽车市场占有率", "新能源汽车技术专利数", "新能源产业增长率",
# "新能源汽车产业链占GDP比值", "交通行业就业指数", "充电桩市场规模",
# "换电站保有量", "智能驾驶乘用车销量", "智能驾驶汽车市场渗透率",
# "空气质量指数", "碳排放量", "可再生能源利用率", "交通事故次数",
# "私人汽车拥有辆", "网约车中新能源汽车占比"
colnames(data) <- c("date",
                    "MS",   # Market Share
                    "TP",   # Tech Patents
                    "IG",   # Industry Growth
                    "IGR",  # Industry GDP Ratio
                    "EI",   # Employment Index
                    "CM",   # Charging Market
                    "SS",   # Swap Stations
                    "AS",   # Autonomous Sales
                    "AM",   # Autonomous Market
                    "AQ",   # Air Quality
                    "CE",   # Carbon Emissions
                    "RU",   # Renewable Usage
                    "AC",   # Accident Count
                    "PC",   # Private Cars
                    "RHS")  # Ride-Hailing NSV Ratio

# 4. 对数据进行标准化处理，消除尺度差异
data_scaled <- as.data.frame(scale(data[-1]))

# 5. 建立多元多变量回归模型
# 以 TP 和 IG 作为预测变量，同时解释其他13个响应变量
response_vars <- c("MS", "IGR", "EI", "CM", "SS", "AS", "AM", "AQ", "CE", "RU", "AC", "PC", "RHS")
formula <- as.formula(paste("cbind(", paste(response_vars, collapse = ", "), ") ~ TP + IG"))
model <- lm(formula, data = data_scaled)

# 输出模型结果
summary(model)

# 6. 提取回归系数（去除截距），构建一个 2x13 的系数矩阵
coef_matrix <- coef(model)[-1,]  # 第一行为截距，剔除
predictors <- rownames(coef_matrix)      # 预测变量：TP、IG
responses <- colnames(coef_matrix)        # 响应变量：其他13个指标
all_nodes <- c(predictors, responses)      # 总节点

# 2. 初始化加权邻接矩阵（所有值初始化为0）
adj_matrix <- matrix(0, nrow = length(all_nodes), ncol = length(all_nodes),
                     dimnames = list(all_nodes, all_nodes))

# 3. 填充邻接矩阵：将预测变量到响应变量的路径权重填入对应位置
for(i in 1:length(predictors)){
  for(j in 1:length(responses)){
    from <- predictors[i]
    to   <- responses[j]
    adj_matrix[from, to] <- coef_matrix[i, j]
  }
}

# 4. 构建边颜色矩阵：正效应蓝色，负效应红色；无边的部分为透明（NA）
edge_color_matrix <- matrix(NA, nrow = length(all_nodes), ncol = length(all_nodes),
                            dimnames = list(all_nodes, all_nodes))
for(i in 1:length(predictors)){
  for(j in 1:length(responses)){
    from <- predictors[i]
    to   <- responses[j]
    weight <- coef_matrix[i, j]
    if(weight > 0) {
      edge_color_matrix[from, to] <- "red"
    } else if(weight < 0) {
      edge_color_matrix[from, to] <- "blue"
    }
  }
}

# 5. 设置节点颜色：预测变量使用深灰色，响应变量使用浅灰色；也可根据需要设置
node_colors <- rep(NA, length(all_nodes))
names(node_colors) <- all_nodes
node_colors[c("MS", "TP")] <- "#00a9c7"
node_colors[c("IG", "IGR", "EI")] <- "#00c4bd"
node_colors[c("CM", "SS", "AS", "AM")] <- "#48dba3"
node_colors[c("AQ", "CE", "RU")] <- "#a4ed84"
node_colors[c("AC", "PC", "RHS")] <- "#f9f871"
node_colors[is.na(node_colors)] <- "gray50"
# 6. 绘制路径图，优化美观效果
library(qgraph)
qgraph(adj_matrix,
       layout = "spring",             # 使用弹簧布局
       labels = all_nodes,            # 节点标签
       label.cex = 1.2,               # 节点标签字号
       vsize = 12,                    # 节点大小
       vTrans = 150,                  # 节点填充透明度
       color = node_colors,           # 节点颜色设置
       edge.labels = round(adj_matrix, 2),  # 显示回归系数
       edge.label.cex = 1.5,          # 边标签字号
       edge.label.position = 0.5,     # 边标签位置居中
       esize = 10,                    # 边宽基础设置
       edge.color = edge_color_matrix,# 边颜色矩阵
       directed = TRUE,               # 有向图
       curve = 0.3,                   # 边曲率，避免重叠
       arrows = TRUE,                 # 显示箭头
       mar = c(5,5,5,5),              # 调整外边距
       legend = FALSE,                 # 显示图例
       legend.mode = "style2",        # 图例风格
       title = "Regression Path Diagram",
       title.cex = 1.5,
       layoutOffset = c(0,0))         # 布局偏移量调整
 
