import matlab.engine
import matlab
import matlab.engine
import numpy as np
eng = matlab.engine.start_matlab()
eng.cd("C:\\Users\\whitefork\\Desktop\\python\\myproject\\test",nargout=0)

label=['正常','短路','开路','阴影']
x_test=[]
y_test=[]
y_pred=[]
result=[]
result1=[]
# 获取 y_pred 结果
[y_test,y_pred]=eng.test(nargout=2)
count=0
count1=0
for temp in y_pred:
    result.append(label[int(temp[0])-1])
    count=count+1
for temp in y_test:
    result1.append(label[int(temp[0])-1])
    
for num in range(0,count):
    if y_test[num]==y_pred[num]:
        count1=count1+1
print("正确率:"+str(count1/count))

print(result1)
print(result)

# 断开与MATLAB引擎的连接
eng.quit()

