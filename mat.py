import pandas as pd
import matplotlib.pyplot as plt 
import matplotlib.style as psl

#魔法命令，用于在笔记本内联显示matplotlib图表
%matplotlib inline 
#确保图表以SVG格式显示
%config InlineBackend.figure_format = 'svg' 

plt.rcParams["font.sans-serif"] = 'Microsoft YaHei' #解决中文乱码问题
plt.rcParams['axes.unicode_minus'] = False #解决负号无法显示

psl.use('ggplot')
plt.figure(figsize=(9, 6)) #设置图表画布大小

#导入数据
df=pd.DataFrame(data={'区域':['华东','华北','东北','西北','西南','华南'],
                      '销售数': np.random.randint(low=100,high=1000,size=6),
                      '销售额': np.random.randint(low=1000,high=10000,size=6)}
               )

x=df['区域'].tolist()
y1=df['销售数'].tolist()
y2=df['销售额'].tolist()

#绘制圆环图
plt.pie(y1,#用于绘制饼图的数据，表示每个扇形的面积
        labels=x,#各个扇形的标签，默认值为 None。
        radius=1.0,#设置饼图的半径，默认为 1
        wedgeprops= dict(edgecolor = "w",width = 0.2),#指定扇形的属性，比如边框线颜色、边框线宽度等
        autopct='%.1f%%',#设置饼图内各个扇形百分比显示格式，%0.1f%% 一位小数百分比
        pctdistance=0.9#指定 autopct 的位置刻度
        )

plt.pie(y2,#用于绘制饼图的数据，表示每个扇形的面积
        #labels=x,
        radius=0.8,#设置饼图的半径，默认为 1
        wedgeprops= dict(edgecolor = "w",width = 0.2),#指定扇形的属性，比如边框线颜色、边框线宽度等
        autopct='%.1f%%',#设置饼图内各个扇形百分比显示格式，%0.1f%% 一位小数百分比
        pctdistance=0.8#指定 autopct 的位置刻度
       )

#设置标题
plt.title("各区域销售数和销售额占比", loc = "center")

#图像展示
plt.show()