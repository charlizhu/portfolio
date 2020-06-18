import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from scipy.signal import find_peaks as fp

thestock = yf.Ticker('CHK') # Change the ticker symbol to what you would like

stockvals = (thestock.history(period='max')['Close']).tolist() # Extracting Values

alldays = (np.linspace(1,len(stockvals),num=len(stockvals))).tolist()

'''
Implement Machine Learning classifier here.
Should be able to recognize the different "vibrational zones" of the stock vs. time.
For now I manually select this time frame.
'''

N = 10 # Constant determining how to take the stock's simple moving average.
averagedstockvals = []
currval = None

# Simple Moving Average
for x in range(N,len(stockvals)):
    currval = sum(stockvals[x-N:x])/N
    averagedstockvals.append(currval)
    currval = None

avgdays = np.linspace(N,len(averagedstockvals),len(averagedstockvals))
avgdays = np.around(avgdays)
avgdays = avgdays.tolist()

# Find max/min vals of averaged values

mindist = None
toppeaks, __ = fp(averagedstockvals,threshold=mindist)
bottompeaks, __ = fp([x * -1 for x in averagedstockvals],threshold=mindist)

# Doing the following to change to ints.
tops = []
bottoms = []
furthestback = 30
mostrecent = 2

topdays = toppeaks[len(toppeaks) - furthestback:len(toppeaks) - mostrecent]
bottomdays = bottompeaks[len(bottompeaks) - furthestback:len(bottompeaks) - mostrecent]

# TO BE CHANGED LATER -- Manually boxed out a time frame
for x in topdays:
    tops.append(averagedstockvals[x])

for x in bottomdays:
    bottoms.append(averagedstockvals[x])

# Linear Regression
minpoints = 10
minR = 0.9
actualtopR = 0
actualbottomR = 0

np_topdays = topdays
np_tops = tops
np_bottomdays = bottomdays
np_bottoms = bottoms

while (len(tops) >= minpoints) and (actualtopR <= minR):
    X = np.array(np_topdays).reshape((-1,1))
    y = np.array(np_tops)

    topmodel = LinearRegression().fit(X,y)

    actualtopR = topmodel.score(X,y)

    np_topdays = np.delete(np_topdays,0)
    np_tops = np.delete(np_tops,0)

while (len(bottoms) >= minpoints) and (actualbottomR <= minR):
    X = np.array(np_bottomdays).reshape((-1, 1))
    y = np.array(np_bottoms)

    bottommodel = LinearRegression().fit(X, y)

    actualbottomR = bottommodel.score(X, y)

    np_bottomdays = np.delete(np_bottomdays,0)
    np_bottoms = np.delete(np_bottoms,0)


print(topmodel.intercept_)
print(topmodel.coef_[0])
print(bottommodel.intercept_)
print(bottommodel.coef_[0])
'''
print(actualtopR)
print(actualbottomR)
print(np_bottomdays)
print(np_topdays)
'''

np_bottomdays = np_bottomdays.tolist()
np_topdays = np_topdays.tolist()

# Plotting
'''
for abscissa1 in np_topdays:
    ordinate1 = topmodel.intercept_ + abscissa1 * topmodel.coef_[0]
    plt.plot(abscissa1,ordinate1)

for abscissa2 in np_bottomdays:
    ordinate2 = bottommodel.intercept_ + abscissa2 * bottommodel.coef_[0]
    plt.plot(abscissa2,ordinate2)
'''

topX1 = np_topdays[0]
topY1 = topmodel.intercept_ + topX1 * topmodel.coef_[0]
topX2 = np_topdays[-1]
topY2 = topmodel.intercept_ + topX2 * topmodel.coef_[0]
botX1 = np_bottomdays[0]
botY1 = bottommodel.intercept_ + botX1 * bottommodel.coef_[0]
botX2 = np_bottomdays[-1]
botY2 = bottommodel.intercept_ + botX2 * bottommodel.coef_[0]

plt.plot([topX1,topX2],[topY1,topY2], color = 'g')
plt.plot([botX1,botX2],[botY1,botY2], color = 'r')
plt.plot(alldays,stockvals,color = '0.5',linewidth = 1.00)
plt.plot(avgdays,averagedstockvals, color = '0.25',linewidth = 0.25)

plt.xlim(6250,7000)
plt.ylim(-250,1500)
plt.show()
