import numpy as np
import matplotlib.pyplot as plt


data = np.loadtxt('./market_data/1min_bar.txt',delimiter=',')
high = data[:,0]
low = data[:,1]
N = len(high)


price = []
gradient = []
curvature = []
for i in range(2,N):
    price.append( high[i] -1030)
    gradient.append( high[i] - high[i-1] )
    curvature.append ( 2* high[i-1] - high[i] - high[i-2] )

gd = np.array(gradient)
cv = np.sign(curvature)
margin = high - low
noise = high[2:-1] - low[1:-2]
print(len(margin[margin>=1]))
print(len(gd[gd>0]))
print(N)


fig=plt.figure()
plt.plot(high,marker='o')
plt.plot(low,marker='o')
plt.grid()
plt.savefig('./output/HighLow.png')

fig=plt.figure()
plt.plot(margin,marker='o')
plt.grid()
plt.savefig('./output/margin.png')

fig=plt.figure()
plt.plot(noise,marker='o')
plt.grid()
plt.savefig('./output/noise.png')

fig=plt.figure(figsize=[20,16])
plt.subplot(2,1,1)
#plt.plot(price,marker='o')
plt.grid()
plt.plot(gd,marker='o',color='red')
#plt.subplot(2,1,2)
#plt.plot(gradient,marker='o',color='red')
#plt.plot(curvature,marker='o', color='red')
#plt.grid()
plt.savefig('./output/price.png',dpi=600)
