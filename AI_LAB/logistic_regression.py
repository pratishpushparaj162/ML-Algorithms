from __future__ import division

m_train = 220
m = 270
n = 13
y_ = []
x_ = [[None for i in range(n)] for j in range(m)]
theta = []
hyp_func = []
for k in range(m_train):
	hyp_func.append(None)
training_file = open("heart-statlog.arff","r")
i=0
for l in training_file:
	if l[0] !='%' and l[0] != '@':
		temp_list = l.split(',')
		# print temp_list
		if temp_list[len(temp_list)-1] == 'present\n':
			y_.append(1)
		else:
			y_.append(0)
		for j in range(len(temp_list)-1):
			x_[i][j] = float(temp_list[j])
		i += 1

avg =[]
rang = []
def mean_norm(x_):
	for i in range(n):
		sum = 0
		for j in range(m):
			sum += x_[j][i]
		avg.append(sum/m)
		maximium = x_[0][i]
		minimium = x_[0][i]
		for j in range(m):
			if x_[j][i] > maximium:
				maximium = x_[j][i]
			if x_[j][i] < minimium:
				minimium = x_[j][i]
		rang.append(maximium-minimium)
		for j in range(m):
			x_[j][i] = (x_[j][i]-avg[i])/rang[i]

def hyp_funct(X):
	hyp_func = 1.0/(1+1.7**(-1.0*X))
	return hyp_func

def der(derivative,l):
	for i in range(m_train):
		derivative += (hyp_func[i]-y[i])*l[i]
	return derivative

mean_norm(x_)
y = y_[:m_train]
x = x_[:m_train]

xc = [[None for i in range(m_train)] for j in range(n)]
for k in range(n):
	for t in range(m_train):
		xc[k][t] = x[t][k]

for j in range(n+1):
	theta.append(j+1)

x0 = [1]*m_train
for k in range(10000):   # No. of iterations
	for j in range(m_train):
		xr = x[j]
		X = 0
		for i in range(n):
			X += theta[i+1]*xr[i]
		X += theta[0]
		hyp_func[j] = hyp_funct(X)
	temp = []

	temp.append(theta[0]-0.01*der(0,x0))

	for i in range(n):
		temp.append(theta[i+1]-0.01*der(0,xc[i]))
	for i in range(n+1):
		theta[i] = temp[i]

print theta
#predict
x_new = x_[m_train:]
y_train = y_[m_train:]
y_test = []
# for i in range(n):
	# x_new.append(float(raw_input()))
# for j in range(n):
	# x_new[j] = (x_new[j]-avg[j])/rang[j]
for j in range(m_test):
	X = 0
	for i in range(n):
		X += theta[i+1]*x_new[j][i]
	X += theta[0]
	if X>=0:
		y_test.append(1)
	else:
		y_test.append(0)
k=0
for j in range(m_test):
	if y_test[j] == y_train[j]:
		k +=1
print k/m_test
