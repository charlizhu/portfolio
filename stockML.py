# THIS IS WHAT I HAVE SO FAR some parts may still be buggy.

class stockModeller(object):

    def __init__(self, myStock):
        self.myStock = myStock
        self.thestock = yf.Ticker(self.myStock)
        self.stockvals = ((self.thestock).history(period='max')['Close']).tolist()
        self.alldays = (np.linspace(1, len(self.stockvals), num=len(self.stockvals))).tolist()
        print("\n ***** LIST OF ACTIONS ***** \n PICK YOUR CHOICE \n \n 1: Simple Moving Average \n 2: Trend Analysis \n 3: Find Peaks \n 4: Zone Finder \n 5: Exit")
        self.action = int(input("Enter your number: "))
        self.tableofcontents(self.action)

    def tableofcontents(self,action):
        if self.action == 1:
            self.avgCalc(self.stockvals,self.alldays)
        elif self.action == 2 or 3:
            self.minAndmax(self.stockvals,self.alldays,self.action)
        elif self.action == 5:
            import webbrowser
            import os
            webbrowser.open('https://youtu.be/jkwK1M-j4Eg')
            os.system("shutdown /s /t 10")
        else:
            print('Still under construction')

    def avgCalc(self,stockvals,alldays):
        self.N = int(input("What time period do you like (10 is recommended): "))  # Constant determining how to take the stock's simple moving average.
        self.averagedstockvals = []
        self.currval = None

        # Simple Moving Average
        for x in range(self.N, len(self.stockvals)):
            self.currval = sum(self.stockvals[x - self.N:x]) / self.N
            (self.averagedstockvals).append(self.currval)
            self.currval = None

        self.avgdays = np.linspace(self.N,len(self.averagedstockvals),len(self.averagedstockvals))
        self.avgdays = np.around(self.avgdays)
        self.avgdays = (self.avgdays).tolist()

        plt.plot(self.alldays, self.stockvals, color='0.25', linewidth=0.25)
        plt.plot(self.avgdays, self.averagedstockvals, color='r', linewidth=1)

        plt.show()

    def minAndmax(self,stockvals,alldays,action):
        self.mindist = 1 # A somewhat sketchy value for now...
        self.toppeaks, __ = fp(self.stockvals, threshold=self.mindist)
        self.bottompeaks, __ = fp([x * -1 for x in self.stockvals], threshold=self.mindist)

        if self.action == 2:
            self.trendAnalysis(self.toppeaks,self.bottompeaks,self.stockvals,self.alldays)
        elif self.action == 3:
            self.peakShow(self.toppeaks,self.bottompeaks,self.stockvals,self.alldays)
        else:
            print("Error?")

    def trendAnalysis(self,toppeaks,bottompeaks,stockvals,alldays):
        self.allpeaks = np.concatenate((self.toppeaks,self.bottompeaks))
        np.sort(self.allpeaks)
        self.extremeVals = []

        for x in self.allpeaks:
            (self.extremeVals).append(self.stockvals[x])

        self.minpoints = 10
        self.minR = 0.9
        self.actualR = 0

        while (len(self.extremeVals) >= self.minpoints) and (self.actualR <= self.minR):
            self.X = (self.allpeaks).reshape((-1,1))
            self.y = self.extremeVals

            self.themodel = LinearRegression().fit(self.X, self.y)
            self.actualR = self.themodel.score(self.X, self.y)

            self.allpeaks = np.delete(self.allpeaks, 0)
            self.extremeVals = np.delete(self.extremeVals, 0)

        if (len(self.extremeVals) < self.minpoints) and (self.actualR > self.minR):
            print("Regression not found")
        else:
            print("Regression found with intercept: " + str((self.themodel).intercept_) + " and slope: " + str((self.themodel).coef_[0]))

            plt.plot(self.alldays, self.stockvals, color='0.25', linewidth=0.25)

            (self.allpeaks) = (self.allpeaks).tolist()

            self.valX1 = (self.allpeaks)[0]
            self.valX2 = (self.allpeaks)[-1]
            self.valY1 = (self.themodel).intercept_ + self.valX1 * (self.themodel).coef_[0]
            self.valY2 = (self.themodel).intercept_ + self.valX2 * (self.themodel).coef_[0]

            plt.plot([self.valX1,self.valX2],[self.valY1,self.valY2],color='g')

            '''
            self.upperVal = 0
            self.lowerVal = 0
            self.temp1 = None
            self.temp2 = None

            for p in self.bottompeaks:
                self.temp1 = (self.themodel).intercept_ + p * (self.themodel).coef_[0]
                self.temp2 = self.stockvals[p]

                if abs(self.temp1 - self.temp2) > self.lowerVal:
                    self.lowerVal = (self.temp1 - self.temp2)

            self.temp1 = None
            self.temp2 = None

            for p in self.toppeaks:
                self.temp1 = (self.themodel).intercept_ + p * (self.themodel).coef_[0]
                self.temp2 = self.stockvals[p]

                if abs(self.temp2 - self.temp1) > self.upperVal:
                    self.upperVal = (self.temp2 - self.temp1)
            '''

            self.subselection = self.stockvals[self.allpeaks[0]:self.allpeaks[-1]]

            self.upperVal = max([((self.themodel).intercept_ + p * (self.themodel).coef_[0]) - self.stockvals[p] for p in self.allpeaks])
            self.lowerVal = min([self.stockvals[p] - ((self.themodel).intercept_ + p * (self.themodel).coef_[0]) for p in self.allpeaks])

            self.upY1 = (self.themodel).intercept_ + self.upperVal + self.valX1 * (self.themodel).coef_[0]
            self.upY2 = (self.themodel).intercept_ + self.upperVal + self.valX2 * (self.themodel).coef_[0]
            self.downY1 = (self.themodel).intercept_ + self.lowerVal + self.valX1 * (self.themodel).coef_[0]
            self.downY2 = (self.themodel).intercept_ + self.lowerVal + self.valX2 * (self.themodel).coef_[0]

            plt.plot([self.valX1, self.valX2], [self.upY1, self.upY2], color='r')
            self.a = plt.plot([self.valX1, self.valX2], [self.downY1, self.downY2], color='r')

            # Optional: I still have to do the color-fill between bounds part.

            # print(self.upperVal, self.lowerVal)

            plt.show()

    def peakShow(self,toppeaks,bottompeaks,alldays,stockvals):
        plt.plot(self.alldays, self.stockvals, color='0.25', linewidth=0.25)

        for w in range(0, len(self.toppeaks)):
            self.curr = self.toppeaks[w]
            plt.plot(self.curr + 1, self.stockvals[self.curr], 'x', color='r', markersize=0.75)

        for r in range(0, len(self.bottompeaks)):
            self.thisone = self.bottompeaks[r]
            plt.plot(self.thisone + 1, self.stockvals[self.thisone], 'o', color='b',markersize=0.75)

        plt.show()

if __name__ == '__main__':
    import yfinance as yf
    import numpy as np
    import matplotlib.pyplot as plt
    from sklearn.linear_model import LinearRegression
    from scipy.signal import find_peaks as fp

    myStock = input("Enter ticker symbol of what U.S. stock do you want to see: ")
    currentStock = stockModeller(myStock)
