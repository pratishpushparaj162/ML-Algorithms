import cv2
import numpy as np
import idx2numpy

SZ=20
bin_n = 16 # Number of bins

svm_params = dict( kernel_type = cv2.SVM_LINEAR,
                    svm_type = cv2.SVM_C_SVC,
                    C=2.67, gamma=5.383 )

affine_flags = cv2.WARP_INVERSE_MAP|cv2.INTER_LINEAR

def deskew(img):
    m = cv2.moments(img)
    if abs(m['mu02']) < 1e-2:
        return img.copy()
    skew = m['mu11']/m['mu02']
    M = np.float32([[1, skew, -0.5*SZ*skew], [0, 1, 0]])
    img = cv2.warpAffine(img,M,(SZ, SZ),flags=affine_flags)
    return img

def hog(img):
    gx = cv2.Sobel(img, cv2.CV_32F, 1, 0)
    gy = cv2.Sobel(img, cv2.CV_32F, 0, 1)
    mag, ang = cv2.cartToPolar(gx, gy)
    bins = np.int32(bin_n*ang/(2*np.pi))    # quantizing binvalues in (0...16)
    bin_cells = bins[:10,:10], bins[10:,:10], bins[:10,10:], bins[10:,10:]
    mag_cells = mag[:10,:10], mag[10:,:10], mag[:10,10:], mag[10:,10:]
    hists = [np.bincount(b.ravel(), m.ravel(), bin_n) for b, m in zip(bin_cells, mag_cells)]
    hist = np.hstack(hists)     # hist is a 64 bit vector
    return hist

img = cv2.imread('digits.png',0)
cells = [np.hsplit(row,100) for row in np.vsplit(img,50)]
train_cells = [ i[:100] for i in cells ]
responses = np.float32(np.repeat(np.arange(10),500)[:,np.newaxis])

ndarr = idx2numpy.convert_from_file('train-images.idx3-ubyte')
response_n=idx2numpy.convert_from_file('train-labels.idx1-ubyte')
test_images = idx2numpy.convert_from_file('t10k-images.idx3-ubyte')
test_label = idx2numpy.convert_from_file('t10k-labels.idx1-ubyte')
response_n=np.float32(response_n[:,np.newaxis])
response_n = np.concatenate((response_n,responses),axis=0)
test_label=np.float32(test_label[:,np.newaxis])
temp=[]
temp2=[]
for j in range(60000):
	temp.append(ndarr[j])
for j in range(10000):
	temp2.append(test_images[j])
k=[]
l=[]
for i in range(600):
	k.append(temp[100*i:100*i+100])
for i in range(100):
	l.append(temp2[100*i:100*i+100])



#######     Now training      ########################
k+=train_cells
deskewed = [map(deskew,row) for row in k]
hogdata = [map(hog,row) for row in deskewed]
trainData = np.float32(hogdata).reshape(-1,64)

svm = cv2.SVM()
svm.train(trainData,response_n, params=svm_params)
svm.save('svm_data_n.dat')

# ######     Now testing      ########################
# cv2.imshow('a',temp2[5000])
# cv2.waitKey(0)
deskewed = [map(deskew,row) for row in l]
hogdata = [map(hog,row) for row in deskewed]
testData = np.float32(hogdata).reshape(-1,bin_n*4)
result = svm.predict_all(testData)
# print result[5000]


# #######   Check Accuracy   ########################
mask = result==test_label
correct = np.count_nonzero(mask)
print correct*100.0/result.size
