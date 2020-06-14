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
for x in range(len(toppeaks) - furthestback,len(toppeaks) - mostrecent):
    tops.append(averagedstockvals[toppeaks[x]])

for x in range(len(bottompeaks) - furthestback,len(bottompeaks) - mostrecent):
    bottoms.append(averagedstockvals[bottompeaks[x]])

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

'''
print(topmodel.intercept_)
print(topmodel.coef_[0])
print(bottommodel.intercept_)
print(bottommodel.coef_[0])
print(actualtopR)
print(actualbottomR)
print(np_bottomdays)
print(np_topdays)
'''

# Plotting
B1 = (np_bottomdays[0]).item()
B2 = (np_bottomdays[len(np_bottomdays) - 1]).item()
bottomdayarray = (np.linspace(B1, B2, num=(B2 - B1 + 1)))

T1 = (np_topdays[0]).item()
T2 = (np_topdays[len(np_topdays) - 1]).item()
topdayarray = (np.linspace(T1, T2, num=(T2 - T1 + 1)))

bottomarray = bottommodel.intercept_ + int(bottommodel.coef_[0]) * bottomdayarray
toparray = topmodel.intercept_ + int(topmodel.coef_[0]) * topdayarray

plt.plot(bottomdayarray,bottomarray,'--')
plt.plot(topdayarray,toparray,'--')
plt.plot(alldays,stockvals)
plt.plot(avgdays,averagedstockvals)

plt.show()