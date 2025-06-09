from pyecharts.charts import Map
from pyecharts import options as opts
from pyecharts.render import make_snapshot
from snapshot_selenium import snapshot
import pandas as pd
from PIL import Image  # 导入PIL库

try:
    province_data = pd.DataFrame({
        'province': ['北京市', '天津市', '吉林省', '上海市', '江苏省', '安徽省', '山东省', '河南省', '广东省', '重庆市', '福建省', '河北省', '内蒙古自治区',
                     '黑龙江省', '浙江省', '湖北省',
                     '湖南省', '广西壮族自治区', '海南省', '四川省', '陕西省', '新疆维吾尔自治区', '山西省'],
        'count': [1, 2, 1, 3, 2, 2, 4, 2, 4, 3, 2, 2, 1, 2, 3, 4, 1, 2, 1, 2, 1, 2, 1]
    })

    # 将数据转换为元组列表，格式为 [(省份, 数量), ...]
    data = list(zip(province_data['province'], province_data['count']))

    # 创建地图对象
    map_chart = Map()

    # 添加数据到地图
    map_chart.add("", data, maptype="china")

    # 设置全局选项，在标题中添加审图号信息，并调整样式和字体大小
    map_chart.set_global_opts(
        title_opts=opts.TitleOpts(
            title="中国地图热力图",
            title_textstyle_opts=opts.TextStyleOpts(font_size=20),  # 缩小标题字体大小
            subtitle_textstyle_opts=opts.TextStyleOpts(font_size=12, color="gray")  # 缩小副标题字体大小并设置颜色
        ),
        visualmap_opts=opts.VisualMapOpts(
            max_=4,
            range_color=["#F5FFFA", "#90EE90"],  # 使用更浅的颜色
            pos_left="10%",
            pos_top="center",
            textstyle_opts=opts.TextStyleOpts(font_size=12)  # 缩小图例字体大小
        ),
        tooltip_opts=opts.TooltipOpts(
            textstyle_opts=opts.TextStyleOpts(font_size=12)  # 缩小提示框字体大小
        )
    )

    # 渲染生成HTML文件
    map_chart.render("china_heatmap.html")

    # 保存为图片
    make_snapshot(snapshot, map_chart.render(), "china_heatmap.png")
    print("地图已保存为china_heatmap.png")

    # 展示图片
    img = Image.open("china_heatmap.png")
    img.show()

except FileNotFoundError:
    print("未找到相关文件，请检查文件路径。")
except Exception as e:
    print(f"发生未知错误: {e}")
