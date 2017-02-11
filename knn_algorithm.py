import cv2
import numpy as np
import matplotlib.pyplot as plt
import math
import operator

def distance(test,point):
	dist=pow(test[0][0]-point[0],2)+pow(test[0][1]-point[1],2)
	return math.sqrt(dist)

def neighbours(test,trainData,k):
	distances=[]
	for i in range(len(trainData)):
		distances.append((trainData[i],distance(test,trainData[i])))
	distances.sort(key=operator.itemgetter(1))
	neighbours=[]
	for i in range(k):
		neighbours.append(distances[i][0])
	return neighbours

def prediction(neighbours,responses,trainData):
	for i in range(len(neighbours)):
		for j in range(len(trainData)):
			if neighbours[i][0]==trainData[j][0] and neighbours[i][1]==trainData[j][1]:
				predict=responses[j]
				return predict 

trainData = np.random.randint(0,100,(25,2)).astype(np.float32)
# Labels each one either Red or Blue with numbers 0 and 1 
responses = np.random.randint(0,2,(25,1)).astype(np.float32)
# Take Red families and plot them 
red = trainData[responses.ravel()==0] 
plt.scatter(red[:,0],red[:,1],80,'r','^')
# Take Blue families and plot them 
blue = trainData[responses.ravel()==1] 
plt.scatter(blue[:,0],blue[:,1],80,'b','s')
# plt.show()
newcomer = np.random.randint(0,100,(1,2)).astype(np.float32)
neighbours=neighbours(newcomer,trainData,3)   # 3 nearest neighbours
print neighbours
result=prediction(neighbours,responses,trainData)
print result
plt.scatter(newcomer[0][0],newcomer[0][1],80)
plt.show()