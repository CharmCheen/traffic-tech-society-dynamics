
library(readxl)
library(dplyr)
library(gRain)
library(igraph)
library(ggraph)
library(ggplot2)
library(infotheo)

# 2. 读取数据并清理缺失值
data_path <- "E:/计算机设计大赛/数据增强后的影响路径数据.xlsx"  # 修改为实际文件路径
raw_data <- read_excel(data_path, sheet = 1)
data_raw <- raw_data %>% na.omit()

# 3. 定义变量名称（节点）
nodes <- c("新能源汽车市场占有率", "新能源汽车技术专利数", 
           "新能源产业增长率", "新能源汽车产业链占GDP比值", "交通行业就业指数",
           "充电桩市场规模", "换电站保有量", "智能驾驶乘用车销量", "智能驾驶汽车市场渗透率",
           "空气质量指数", "碳排放量", "可再生能源利用率",
           "交通事故次数", "私人汽车拥有辆", "网约车中新能源汽车占比")

# 4. 选择所需数据列
data_model <- data_raw[, nodes]

# 5. 离散化处理：将连续变量按等频分为3档（low, medium, high）
data_disc <- data_model %>%
  mutate(across(everything(),
                ~ cut(.x,
                      breaks = quantile(.x, probs = seq(0, 1, length.out = 4), na.rm = TRUE),
                      include.lowest = TRUE,
                      labels = c("low", "medium", "high")
                )
  )
  )

# 6. 构建 DAG（假设“新能源汽车市场占有率”和“新能源汽车技术专利数”为外生变量）
parent_nodes <- c("新能源汽车市场占有率", "新能源汽车技术专利数")
dag_model <- igraph::graph.empty(n = length(nodes), directed = TRUE)
V(dag_model)$name <- nodes
for(child in setdiff(nodes, parent_nodes)) {
  for(p in parent_nodes) {
    dag_model <- igraph::add_edges(dag_model, c(which(V(dag_model)$name == p),
                                                which(V(dag_model)$name == child)))
  }
}

# 可视化基础 DAG（无互信息权重）
plot(dag_model, vertex.size = 20, vertex.color = "lightblue", vertex.label.cex = 0.8, edge.arrow.size = 0.5)

# 7. 定义构建 CPT 的函数（针对离散化后的因子变量），并添加拉普拉斯平滑
make_cpt <- function(data, child, parents = NULL, laplace = 1) {
  if (is.null(parents)) {
    # 无父节点：计算 child 的频数，加上平滑项
    freq <- table(data[[child]]) + laplace
    prob <- as.numeric(freq) / sum(freq)
    fmla <- as.formula(paste("~", paste0("`", child, "`")))
    cpt_obj <- cptable(fmla, values = prob, levels = levels(data[[child]]))
  } else {
    all_vars <- c(child, parents)
    # 计算联合频数并加上平滑项
    tab <- table(data[, all_vars]) + laplace
    # 归一化：对每个父节点组合归一化 child 维度
    pt <- prop.table(tab, margin = seq(2, length(dim(tab))))
    fmla <- as.formula(paste("~", paste0("`", child, "`"), "|",
                             paste(paste0("`", parents, "`"), collapse = " + ")))
    cpt_obj <- cptable(fmla, values = as.numeric(pt), levels = levels(data[[child]]))
  }
  return(cpt_obj)
}

# 8. 构建所有节点的 CPT 列表
cpt_list <- list()
# 外生变量（无父节点）的 CPT
for (v in parent_nodes) {
  cpt_list[[v]] <- make_cpt(data_disc, child = v)
}
# 其他变量，以外生变量为父节点
other_nodes <- setdiff(nodes, parent_nodes)
for (v in other_nodes) {
  cpt_list[[v]] <- make_cpt(data_disc, child = v, parents = parent_nodes)
}

# 可选：检查某一节点的 CPT（例如“新能源产业增长率”的 CPT）
print("新能源产业增长率的 CPT:")
print(cpt_list[["新能源产业增长率"]])

# 9. 编译 CPT 列表并构建贝叶斯网络模型
compiledCPT <- compileCPT(cpt_list)
bn_model <- grain(compiledCPT)
bn_model <- compile(bn_model)

# 10. 推断示例：设“新能源汽车技术专利数”为 "high"，查询“新能源产业增长率”的后验分布
bn_ev <- setEvidence(bn_model, nodes = "新能源汽车技术专利数", states = "high")
result <- querygrain(bn_ev, nodes = "新能源产业增长率", type = "marginal")
print("条件推断结果：当新能源汽车技术专利数为 high 时，新能源产业增长率的后验分布：")
print(result)

# 11. 基于互信息构建网络可视化
edge_list <- data.frame(from = character(), to = character(), mi = numeric(), stringsAsFactors = FALSE)
for(child in setdiff(nodes, parent_nodes)) {
  for(p in parent_nodes) {
    mi_value <- infotheo::mutinformation(data_disc[[p]], data_disc[[child]])
    edge_list <- rbind(edge_list, data.frame(from = p, to = child, mi = mi_value, stringsAsFactors = FALSE))
  }
}

g <- graph_from_data_frame(d = edge_list, 
                           vertices = data.frame(name = nodes, stringsAsFactors = FALSE), 
                           directed = TRUE)

# 改进的贝叶斯网络可视化
library(ggplot2)
library(ggraph)
library(viridis)

p <- ggraph(g, layout = "fr") +
  # 绘制边，采用灰色，宽度依据互信息数值调整，箭头加粗、圆形终端
  geom_edge_link(aes(width = mi), edge_color = "#a6cee3",
                 arrow = arrow(length = unit(5, 'mm')), 
                 end_cap = circle(5, 'mm')) +
  # 绘制节点，使用填充色，黑色边框，圆形节点
  geom_node_point(aes(fill = name), shape = 21, size = 8, color = "black", stroke = 0.5) +
  # 绘制节点标签，使用 Helvetica 字体，避免重叠，颜色深灰
  geom_node_text(aes(label = name), repel = TRUE, size = 8, 
                 family = "Helvetica", fontface = "bold", color = "#333333") +
  # 调整边宽比例
  scale_edge_width(range = c(0.8, 4)) +
  # 使用 Viridis 离散调色板，美化节点填充色
  scale_fill_viridis_d(option = "D") +
  # 使用极简主题，并去除背景网格
  theme_void() +
  # 添加标题，并调整标题样式符合期刊要求
  ggtitle("Bayesian Network Structure") +
  theme(
    plot.title = element_text(family = "Helvetica", face = "bold", size = 20, hjust = 0.5, margin = margin(b = 10)),
    legend.position = "none",
    plot.background = element_rect(fill = "white", color = NA)
  )

print(p)

