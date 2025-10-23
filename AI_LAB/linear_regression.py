from __future__ import division

m_test = 0
m_train = 20
m = 20
n = 1
y_ = []
x_ = [[None for i in range(n)] for j in range(m)]
training_file = open("dataset_1","r")
i=0
for l in training_file:
	if l[0] !='%' and l[0] != '@' and l[0] != '\n':
		temp_list = l.split(',')
		# print temp_list
		y_.append(float(temp_list[len(temp_list)-1]))
		for j in range(len(temp_list)-1):
			x_[i][j] = float(temp_list[j])
		i += 1

avg =[]
rang = []
def mean_norm_x(x):
	for i in range(n):
		sum = 0
		for j in range(m_train):
			sum += x[j][i]
		avg.append(sum/m_train)
		maximium = x[0][i]
		minimium = x[0][i]
		for j in range(m_train):
			if x[j][i] > maximium:
				maximium = x[j][i]
			if x[j][i] < minimium:
				minimium = x[j][i]
		rang.append(maximium-minimium)
		for j in range(m_train):
			if rang[i] != 0:
				x[j][i] = (x[j][i]-avg[i])/rang[i]

def der(derivative,l):
	for j in range(m_train):
		derivative += (hyp_func[j]-y[j])*l[j]
	return 1.0/m_train*derivative

def cost():
	cost=0
	for j in range(m_train):
		cost += (hyp_func[j]-y[j])*(hyp_func[j]-y[j])
	return cost

#train_data
y = y_[:m_train]
x = x_[:m_train]

# mean_norm_x(x)
theta = []
for j in range(n+1):
	theta.append(j+1)
hyp_func = []
for k in range(m_train):
	hyp_func.append(None)
xc = [[None for i in range(m_train)] for j in range(n)]
for k in range(n):
	for t in range(m_train):
		xc[k][t] = x[t][k]
x0 = [1]*m_train

cost_function = 10000000000
while 1:
	for j in range(m_train):
		xr = x[j]
		X = 0
		for i in range(n):
			X += theta[i+1]*xr[i]
		X += theta[0]
		hyp_func[j] = X
	temp = []
	#for theta[0]
	temp.append(theta[0]-0.001*der(0,x0))
	for i in range(n):
		temp.append(theta[i+1]-0.01*der(0,xc[i]))
	for i in range(n+1):
		theta[i] = temp[i]
	print theta
	cost_function_ = 1/(2*m_train)*cost()
	if cost_function-cost_function_ < 0.00000001:
		break
	if cost_function_<cost_function:
		# print cost_function_
		cost_function = cost_function_
		continue
print theta


