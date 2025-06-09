
library(readxl)
library(dplyr)
library(gRain)
library(ggplot2)
library(ggraph)
library(igraph)
library(tidygraph)
library(RColorBrewer)
data_path <- "E:/计算机设计大赛/影响路径.xlsx"
raw_data <- read_excel(data_path, sheet = 1)
str(raw_data)
head(raw_data)
data_clean <- raw_data %>% na.omit()
# 技术创新指标
tech_vars <- data_clean %>% select(新能源汽车市场占有率, 新能源汽车技术专利数)
# 经济与产业结构指标
econ_vars <- data_clean %>% select(新能源产业增长率, 新能源汽车产业链占GDP比值, 交通行业就业指数)
# 基础设施指
infra_vars <- data_clean %>% select(充电桩市场规模, 换电站保有量, 智能驾驶乘用车销量, 智能驾驶汽车市场渗透率)
# 环境与可持续发展指标
env_vars <- data_clean %>% select(空气质量指数, 碳排放量, 可再生能源利用率)
# 社会生活指标
social_vars <- data_clean %>% select(交通事故次数, 私人汽车拥有辆, 网约车中新能源汽车占比)
data_model <- bind_cols(tech_vars, econ_vars, infra_vars, env_vars, social_vars)
data_disc <- data_model %>% mutate_all(function(x){
  # 使用 quantile 分位点，注意去除 NA
  q <- quantile(x, probs = c(0, 1/3, 2/3, 1), na.rm = TRUE)
  # 如果分位数有重复值，确保区间合理
  cut(x, breaks = unique(q), include.lowest = TRUE, labels = c("低","中","高"))
})
nodes <- c("新能源汽车市场占有率", "新能源汽车技术专利数", 
           "新能源产业增长率", "新能源汽车产业链占GDP比值", "交通行业就业指数",
           "充电桩市场规模", "换电站保有量", "智能驾驶乘用车销量", "智能驾驶汽车市场渗透率",
           "空气质量指数", "碳排放量", "可再生能源利用率",
           "交通事故次数", "私人汽车拥有辆", "网约车中新能源汽车占比")

parent_nodes <- c("新能源汽车市场占有率", "新能源汽车技术专利数")
make_cpt <- function(data, child, parents = NULL) {
  if (is.null(parents)) {
    # 无父节点：计算边际概率
    freq <- table(data[[child]])
    prob <- freq / sum(freq)
    # 创建数组，保证维度名称
    cpt_array <- array(prob, dim = length(prob), dimnames = list(child = names(prob)))
  } else {
    # 有父节点：构造频数表，formula 格式如 ~ Parent1 + Parent2 + Child
    formula_str <- as.formula(paste("~", paste(c(parents, child), collapse = "+")))
    freq <- xtabs(formula_str, data = data)
    # 对每一组父节点配置归一化
    margin_dims <- seq_along(parents)
    prob <- prop.table(freq, margin = margin_dims)
    cpt_array <- as.array(prob)
  }
  return(cpt_array)
}
cpt_list <- list()
for (node in c("新能源汽车市场占有率", "新能源汽车技术专利数")) {
  cpt_list[[node]] <- make_cpt(data_disc, child = node)
}

# 对其他节点（均以技术创新指标为父节点）
other_nodes <- setdiff(nodes, c("新能源汽车市场占有率", "新能源汽车技术专利数"))
for (node in other_nodes) {
  cpt_list[[node]] <- make_cpt(data_disc, child = node, parents = parent_nodes)
}

# 查看部分 CPT（例如新能源产业增长率的 CPT）
print("新能源产业增长率的 CPT:")
print(cpt_list[["新能源产业增长率"]])
# 这里将每个数组赋予 class "cptable"
cpt_list <- lapply(cpt_list, function(x) { class(x) <- "cptable"; return(x) })
# 利用 compileCPT() 将 CPT 列表编译为适合 grain() 构造的对象
compiledCPT <- compileCPT(cpt_list)
# 将 CPT 列表组合到一起，注意各 CPT 名称需与节点名一致
bn_grain <- grain(compiledCPT)
bn_grain <- compile(bn_grain)

bn_grain_ev <- setEvidence(bn_grain, nodes = "新能源汽车技术专利数", states = "高")
query_result <- querygrain(bn_grain_ev, nodes = "新能源产业增长率", type = "marginal")
print("条件推断：当新能源汽车技术专利数为 '高' 时，新能源产业增长率的分布：")
print(query_result)

# 网络结构可视化
# 所有非技术创新指标均有两条边，来自“新能源汽车市场占有率”和“新能源汽车技术专利数”
edge_list <- data.frame(
  from = rep(parent_nodes, times = length(other_nodes)),
  to = rep(other_nodes, each = length(parent_nodes)),
  stringsAsFactors = FALSE
)
g <- graph_from_data_frame(edge_list, vertices = nodes, directed = TRUE)
# 将 igraph 转为 tidygraph 对象，方便 ggraph 绘图
tg <- as_tbl_graph(g)
node_groups <- data.frame(
  node = nodes,
  group = case_when(
    node %in% c("新能源汽车市场占有率", "新能源汽车技术专利数") ~ "技术创新",
    node %in% c("新能源产业增长率", "新能源汽车产业链占GDP比值", "交通行业就业指数") ~ "经济与产业结构",
    node %in% c("充电桩市场规模", "换电站保有量", "智能驾驶乘用车销量", "智能驾驶汽车市场渗透率") ~ "基础设施",
    node %in% c("空气质量指数", "碳排放量", "可再生能源利用率") ~ "环境与可持续发展",
    node %in% c("交通事故次数", "私人汽车拥有辆", "网约车中新能源汽车占比") ~ "社会生活",
    TRUE ~ "其他"
  ),
  stringsAsFactors = FALSE
)

# 将分组信息加入节点属性
tg <- tg %>% activate(nodes) %>% left_join(node_groups, by = c("name" = "node"))

# 定义调色板
group_colors <- c("技术创新" = "#1b9e77", 
                  "经济与产业结构" = "#d95f02",
                  "基础设施" = "#7570b3",
                  "环境与可持续发展" = "#e7298a",
                  "社会生活" = "#66a61e",
                  "其他" = "gray")

# 绘制高质量网络图（采用 Fruchterman-Reingold 布局，风格尽量接近 Nature 杂志）
p <- ggraph(tg, layout = "fr") +
  geom_edge_link(aes(edge_alpha = 0.8), color = "grey50", show.legend = FALSE) +
  geom_node_point(aes(color = group), size = 6) +
  geom_node_text(aes(label = name), repel = TRUE, size = 4, color = "black") +
  scale_color_manual(values = group_colors) +
  theme_minimal(base_size = 14) +
  theme(
    panel.grid = element_blank(),
    legend.title = element_blank(),
    plot.title = element_text(hjust = 0.5, face = "bold")
  ) +
  labs(title = "技术创新对社会变革各指标影响的贝叶斯网络模型")

# 保存高分辨率图像
ggsave("Bayesian_Network_NatureStyle.png", plot = p, width = 10, height = 8, dpi = 300)

# 显示图形
print(p)






