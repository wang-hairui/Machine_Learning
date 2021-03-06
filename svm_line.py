import numpy as np
import sklearn.model_selection as ms
import sklearn.svm as svm
import sklearn.metrics as sm
import matplotlib.pyplot as mp

x,y=[],[]
with open('../data/multiple2.txt','r') as f:
    for line in f.readlines():
        data=[float(substr) for substr in line.split(",")]
        #输入
        x.append(data[:-1])
        #输出
        y.append(data[-1])
#处理数据为数组
x=np.array(x)
y=np.array(y,dtype=int)
train_x,test_x,train_y,test_y=ms.train_test_split(x,y,test_size=0.25,random_state=5)
#SVC---支持向量分类,参数为什么核函数
model=svm.SVC(kernel='linear')
#拟合训练数据
model.fit(train_x,train_y)
#画栅格所需的边界数据
r,l,h=x[:,0].min()-1,x[:,0].max()+1,0.005
b,t,v=x[:,1].min()-1,x[:,1].max()+1,0.005
#生成栅格的点阵数据列表,meshgrid存在于数据numpy模块，不是画图模块
grid_x=np.meshgrid(np.arange(r,l,h),np.arange(b,t,v))
# print(type(grid_x))
#将数据平展开，拼接成为数组,np.c_[]函数是中括号，类似于array的功能
flat_x=np.c_[grid_x[0].ravel(),grid_x[1].ravel()]
# print(type(flat_x))
#对训练集进行预测,生成一个数组的类型
flat_y=model.predict(flat_x)
# print(type(flat_y))
#将输出数组也栅格化，便于画图
grid_y=flat_y.reshape(grid_x[0].shape)

#查看一下分类报告
test_pred_y=model.predict(test_x)
cr=sm.classification_report(test_y,test_pred_y)
print(cr)


mp.figure('SVM Linear Classification',facecolor='lightgray')

mp.title('SVM Linear Classification',fontsize=20)
mp.xlabel('x',fontsize=14)
mp.ylabel('y',fontsize=14)
mp.tick_params(labelsize=10)
#画一条分割线进行分类,y的值只有两类，所以颜色映射只要写一类就行
mp.pcolormesh(grid_x[0],grid_x[1],grid_y,cmap='gray')
mp.xlim(grid_x[0].min(),grid_x[0].max())
mp.ylim(grid_x[1].min(),grid_x[1].max())

#两种类别的掩码，得到掩码数组
C0,C1=y==0,y==1
# print(x[C0])
# print(x[C0][:,0],x[C0][:,1])
mp.scatter(x[C0][:,0],x[C0][:,1],c='orangered',s=80)
mp.scatter(x[C1][:,0],x[C1][:,1],c='red',s=80)
mp.show()


