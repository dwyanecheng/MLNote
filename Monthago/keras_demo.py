
import pandas as pd 
import numpy as np 
from keras.models import Sequential
from keras.layers import Dense,Activation,Dropout

data = pd.read_csv('data\creditcard.csv')  #读取数据
class1 = data[data.Class == 0]  #负样本 欺诈
class2 = data[data.Class == 1]  #正样本 不欺诈

data1 = class1.values
data2 = class2.values

#数据处理 正负样本比例1:10 
idx1 = np.random.randint(200000)
idx2 = np.random.randint(200)
feedx = np.concatenate([data1[idx1:idx1+2000, 1:29], data2[idx2:idx2+200, 1:29]]) 
feedy = np.zeros([2200, 2])
feedy[:2000, 0] = 1
feedy[2000:, 1] = 1

#添加测试集后面的25条负样本与25条正样本
test_x = np.concatenate([data1[idx1+2000:idx1+2025, 1:29], data2[idx2+200:idx2+225, 1:29]]) 
test_y = np.zeros([50, 2])
test_y[:25, 0] = 1
test_y[25:, 1] = 1

# print(len(class1))
# print(len(class2))

model = Sequential()  #初始化模型

#第一层网络
model.add(Dense(28 , input_shape = (28 , )))
#常用激活函数，http://keras-cn.readthedocs.io/en/latest/other/activations/
model.add(Activation('relu'))  # sigmod 
model.add(Dropout(0.2))

#第二层网络
model.add(Dense(20))
model.add(Activation('relu'))
model.add(Dropout(0.2))

#第三层网络
model.add(Dense(10))
model.add(Activation('relu'))
model.add(Dropout(0.2))

#第四层网络
model.add(Dense(5))
model.add(Activation('relu'))
model.add(Dropout(0.2))

#输出
model.add(Dense(2))
model.add(Activation('softmax'))

model.summary()
#优化器optimizers常用见文档http://keras-cn.readthedocs.io/en/latest/other/objectives/
#损失函数，常用http://keras-cn.readthedocs.io/en/latest/other/objectives/
model.compile(loss='categorical_crossentropy', optimizer = 'adam' , metrics=['accuracy'])  
model.fit(feedx, feedy, batch_size=200, epochs= 10, verbose = 1)

score = model.evaluate(test_x,test_y, verbose=1)

#score[0]是损失loss,score[1]是准确率accuracy
print('test_score :',score[0])
print('test_accuracy :',score[1])


"""
正负样本比例1:10  网络层数2层
test_score : 0.580577712059
test_accuracy : 0.780000009537

正负样本比例1:10  网络层数3层
test_score : 0.203649388552
test_accuracy : 0.919999990463

正负样本比例1:10  网络层数4层
test_score : 2.11679269791
test_accuracy : 0.740000002384

"""

import matplotlib.pyplot as plt 
x_prt = [2,3,4]
test_score = [0.580577712059,0.203649388552,2.11679269791]
test_accuracy = [0.780000009537,0.919999990463,0.740000002384]

plt.figure()
plt.plot(x_prt, test_score , c = 'g' , label = 'test_score', linewidth = 2)
plt.plot(x_prt, test_accuracy , c = 'r' , label = 'test_accuracy' , linewidth = 2)
plt.xlabel('x_prt')
plt.ylabel('target')
plt.title("Keras layer 2-3-4")
plt.legend()
plt.show()