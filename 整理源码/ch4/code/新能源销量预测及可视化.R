library(tidyselect)
library(tidyverse)
library(grid)
data_long <- data %>%
  pivot_longer(cols = c(新能源汽车产量, 新能源汽车销量, 
                        纯电动汽车产量, 纯电动汽车销量, 
                        插电式混合动力汽车产量, 插电式混合动力汽车销量),
               names_to = "指标", values_to = "万辆数") %>%
  mutate(数据来源 = "数据1")

colors <- c("新能源汽车产量" = "#0072B2", 
            "新能源汽车销量" = "#D55E00", 
            "纯电动汽车产量" = "#009E73", 
            "纯电动汽车销量" = "#F0E442", 
            "插电式混合动力汽车产量" = "#56B4E9", 
            "插电式混合动力汽车销量" = "#E69F00")
diff_data <- data %>%
  transmute(
    时间,
    `新能源汽车产销差额` = (新能源汽车产量 - 新能源汽车销量) * 10,
    `纯电动汽车产销差额` = (纯电动汽车产量 - 纯电动汽车销量) * 10,
    `插电式混合动力汽车产销差额` = (插电式混合动力汽车产量 - 插电式混合动力汽车销量) * 10
  ) %>%
  pivot_longer(cols = -时间, names_to = "指标", values_to = "差额") %>%
  mutate(数据来源 = "产销差额")
p_main <- ggplot(data_long, aes(x = 时间, y = 万辆数, color = 指标)) +
  geom_line(size = 1.2) + 
  geom_point(size = 3) +
  labs(title = "全国新能源汽车及细分类型产销量趋势",
       x = "时间",
       y = "万辆数",
       color = "指标") +
  scale_color_manual(values = colors) +
  theme_minimal(base_size = 14) +
  theme(
    plot.title = element_text(hjust = 0.5, face = "bold"),
    axis.title = element_text(face = "bold"),
    legend.position = "top"
  )
p_diff <- ggplot(diff_data, aes(x = 时间, y = 差额, color = 指标)) +
  geom_line(size = 1) +
  geom_point(size = 2) +
  labs(title = "产销差额趋势", x = NULL, y = "差额（千辆）") +
  scale_color_manual(values = c("新能源汽车产销差额" = "#0072B2", 
                                "纯电动汽车产销差额" = "#009E73", 
                                "插电式混合动力汽车产销差额" = "#56B4E9")) +
  scale_y_continuous(limits = c(-20, 40), breaks = seq(-20, 40, by = 10)) +
  theme_minimal(base_size = 10) +
  theme(
    plot.title = element_text(hjust = 0.5),
    legend.position = "bottom",
    axis.text.x = element_text(angle = 45, hjust = 1)
  )
p_main +
  annotation_custom(
    ggplotGrob(p_diff),
    xmin = as.POSIXct("2018-06-01"),   # 根据数据时间范围调整
    xmax = as.POSIXct("2019-06-01"),     # 调整宽度
    ymin = 40,                          # 根据主图y轴范围调整
    ymax = 60                           # 调整高度
  )





