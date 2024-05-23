import matlab.engine
import matlab
import matlab.engine
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
plt.rcParams['font.sans-serif'] = ['SimHei']
        # 解决无法显示负号
plt.rcParams['axes.unicode_minus'] = False
eng = matlab.engine.start_matlab()
eng.cd("C:\\Users\\whitefork\\Desktop\\python\\myproject\\test1",nargout=0)
label0=['正常','短路','开路','阴影']
label=['准确率','精确率','召回率','F1分数']
ratio=[]
accuracy=[]
precision=[]
recall=[]
f1score=[]
m=[]

my_v=[]
my_i=[]
my_state=[]
# 获取 y_pred 结果
[my_v,my_i,my_state,m,ratio,accuracy,precision,recall]=eng.test1(nargout=8)

print(recall)
width = 0.35
data=[]
for i in range(0,4):
    data.append(ratio[i][0])
# 将bottom_y元素都初始化为0
bottom_y = np.zeros(1)
x=range(1)
label=['1']
data=np.array(data)
# 按列计算计算每组柱子的总和，为计算百分比做准备
sums = np.sum(data)
for i in data:
    # 计算每个柱子的高度，即百分比
    y = i / sums
    plt.bar(x, data, width, bottom=bottom_y)
    # 计算bottom参数的位置
    bottom_y = y + bottom_y
plt.xticks(x, label)

plt.show()






M=np.array(m,dtype=np.int64)

for i in range(0,len(ratio)):
    print(label0[i]+": "+str(ratio[i][0]))

print(accuracy)
print(precision)
print(recall)

classes = ["正常","短路","开路","阴影"]
proportion = []
length = len(M)
for i in M:
    for j in i:
        temp = j / (np.sum(i))
        proportion.append(temp)
# print(np.sum(M[0]))
# print(proportion)
pshow = []
for i in proportion:
    pt = "%.2f%%" % (i * 100)
    pshow.append(pt)
proportion = np.array(proportion).reshape(length, length)  # reshape(列的长度，行的长度)
pshow = np.array(pshow).reshape(length, length)
# print(pshow)

plt.imshow(proportion, interpolation='nearest', cmap=plt.cm.Blues)  # 按照像素显示出矩阵
# (改变颜色：'Greys', 'Purples', 'Blues', 'Greens', 'Oranges', 'Reds','YlOrBr', 'YlOrRd',
# 'OrRd', 'PuRd', 'RdPu', 'BuPu','GnBu', 'PuBu', 'YlGnBu', 'PuBuGn', 'BuGn', 'YlGn')
# plt.title('M')
#plt.colorbar()
tick_marks = np.arange(len(classes))
plt.xticks(tick_marks, classes, fontsize=12)
plt.yticks(tick_marks, classes, fontsize=12)

thresh = M.max() / 2.
# iters = [[i,j] for i in range(len(classes)) for j in range((classes))]

iters = np.reshape([[[i, j] for j in range(length)] for i in range(length)], (M.size, 2))
for i, j in iters:
    if (i == j):
        plt.text(j, i - 0.12, format(M[i, j]), va='center', ha='center', fontsize=10, color='white',
                 weight=5)  # 显示对应的数字

    else:
        plt.text(j, i - 0.12, format(M[i, j]), va='center', ha='center', fontsize=10)  # 显示对应的数字


plt.ylabel('True label', fontsize=16)
plt.xlabel('Predict label', fontsize=16)
plt.tight_layout()
plt.show()








# 断开与MATLAB引擎的连接
eng.quit()

