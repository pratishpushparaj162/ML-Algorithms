import cv2
import numpy as np

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

# First half is trainData, remaining is testData
train_cells = [ i[:100] for i in cells ]
# test_cells = [ i[50:] for i in cells]

######     Now training      ########################

deskewed = [map(deskew,row) for row in train_cells]
hogdata = [map(hog,row) for row in deskewed]
trainData = np.float32(hogdata).reshape(-1,64)
responses = np.float32(np.repeat(np.arange(10),500)[:,np.newaxis])

svm = cv2.SVM()
svm.train(trainData,responses, params=svm_params)
svm.save('svm_data.dat')

######     Now testing      ########################

# deskewed = [map(deskew,row) for row in test_cells]
# hogdata = [map(hog,row) for row in deskewed]
# testData = np.float32(hogdata).reshape(-1,bin_n*4)
test=cv2.imread('0.png')
gray = cv2.cvtColor(test,cv2.COLOR_BGR2GRAY)
gray= cv2.resize(gray,(20,20),interpolation=cv2.INTER_AREA)
ret,gray = cv2.threshold(gray,10,255,cv2.THRESH_BINARY)
kernel=np.ones((2,2),np.uint8)
gray=cv2.dilate(gray,kernel,iterations=1)
gray = cv2.erode(gray,kernel,iterations=1)
cv2.imshow('kk',gray)
cv2.waitKey(20)
test_cells=[np.hsplit(row,1) for row in np.vsplit(gray,1)]
deskewed = [map(deskew,row) for row in test_cells]
print deskewed
hogdata = [map(hog,row) for row in deskewed]
testData = np.float32(hogdata).reshape(-1,bin_n*4)
result = svm.predict_all(testData)

print result



# #######   Check Accuracy   ########################
# mask = result==responses
# correct = np.count_nonzero(mask)
# print correct*100.0/result.size
