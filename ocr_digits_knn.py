import numpy as np
import cv2 
from matplotlib import pyplot as plt



img = cv2.imread('digits.png')
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
# Now we split the image to 5000 cells, each 20x20 size 
cells = [np.hsplit(row,100) for row in np.vsplit(gray,50)]
# Make it into a Numpy array. It size will be (50,100,20,20) 
x = np.array(cells)
# Now we prepare train_data and test_data. 
train = x[:,:].reshape(-1,400).astype(np.float32)
k = np.arange(10) 
train_labels = np.repeat(k,500)[:,np.newaxis]
# Initiate kNN, train the data, then test it with test data for k=1 
knn = cv2.KNearest()
knn.train(train,train_labels)
test=cv2.imread('4.png')
gray2 = cv2.cvtColor(test,cv2.COLOR_BGR2GRAY)
gray2 = cv2.resize(gray2,(20,20),interpolation=cv2.INTER_AREA)
ret,gray2 = cv2.threshold(gray2,10,255,cv2.THRESH_BINARY)
cv2.imshow('kk',gray2)
cv2.waitKey(0)
kernel=np.ones((2,2),np.uint8)
gray2=cv2.dilate(gray2,kernel,iterations=1)
gray2 = cv2.erode(gray2,kernel,iterations=1)
cv2.imshow('kk',gray2)
cv2.waitKey(0)
final=gray2.reshape(-1,400).astype(np.float32)
ret,result,neighbours,dist = knn.find_nearest(final,k=20)
# save the data 
print result 
print neighbours
np.savez('knn_data.npz',train=train, train_labels=train_labels)
# Now load the data 
with np.load('knn_data.npz') as data: 
	train = data['train'] 
	train_labels = data['train_labels']
