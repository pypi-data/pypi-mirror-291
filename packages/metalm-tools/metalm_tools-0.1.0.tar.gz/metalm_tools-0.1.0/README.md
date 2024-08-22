# MetaLM-tools

metalm的工具集，当前只有代码解释器这一个工具。


案例：
```
from metalm_tools import MetaLMInterpreterTool
import time 
import json

packages=['numpy','pandas']
#画图
c = """
import matplotlib.pyplot as plt
import time

# 数据
x = [1, 2, 3, 4, 5]
y = [1, 4, 9, 16, 25]

# 创建折线图
plt.plot(x, y, marker='o')

# 添加标题和轴标签
plt.title("Simple Line Plot")
plt.xlabel("X Axis")
plt.ylabel("Y Axis")

# 显示图形
plt.grid(True)  # 显示网格线
plt.show()
plt.savefig('test1.png')
x = [1, 2, 3, 4, 5]
y = [1, 4, 9, 16, 25]

# 创建折线图
plt.plot(x, y, marker='o')

# 添加标题和轴标签
plt.title("Simple Line Plot")
plt.xlabel("X Axis")
plt.ylabel("Y Axis")

# 显示图形
plt.grid(True)  # 显示网格线
plt.show()
plt.savefig('test2.png')

for i in x:
    print(i)
    time.sleep(1)
"""
#操作csv
c2 = """
import pandas as pd

# 读取CSV文件
df = pd.read_csv('/codebox/1.csv')

# 获取前5行
df_first_five = df.head(5)

# 保存前5行到新的CSV文件
df_first_five.to_csv('output_file.csv', index=False)

print("前5行已保存到 'output_file.csv'")

"""

tool = MetaLMInterpreterTool('http://10.88.36.58:5002','empty')
print(tool.session.session_id)
tool.install_python_packages(packages)
res1 = tool.upload_files(['/data/jueyuan/project/test/1.csv'],['这是要分析的数据'])
res2 = tool.upload_files(['/data/jueyuan/project/test/image.png'],['这是图片'])
print('path:',res1,res2)
rsp = tool._run(c2)
rsp = json.loads(rsp)
print(rsp)
tbyte = tool.download_files(['output_file.csv'])
print(tbyte)

rsp = tool._run(c)
rsp = json.loads(rsp)
print(rsp)

tool.close()
```