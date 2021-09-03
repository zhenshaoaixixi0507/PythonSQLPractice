import pandas as pd
import matplotlib.pyplot as plt
import statistics
def Calculate3MonthReturn(data):
    returns=[data[i+1]/data[i]-1 for i in range(len(data)-1)]
    return sum(returns) / len(returns)

def Calculate3MonthSharpRate(data):
    returns=[data[i+1]/data[i]-1 for i in range(len(data)-1)]
    return sum(returns) / len(returns)/statistics.stdev(returns)

def CalculatePortfolioReturn(portfolio):
    returns=[]
    for i in range(len(portfolio[0])):
        returns.append(portfolio[1][i]/portfolio[0][i]-1)
    return sum(returns)/len(returns)

df = pd.read_excel ('FidelityHistoricalData.xlsx')
rollingwindow=4
holdingperiod=3
numOfFunds=5
rows=len(df)
columns=len(df.columns)
fundList=[]
portfolioRet=[]
initialValue=1000
for i in range(rows-rollingwindow):
    if i% holdingperiod == 0:
        averageretList=[]
        for j in range(columns-1):
            subsetindices=[k+i for k in range(rollingwindow)]
            averageretList.append(Calculate3MonthReturn(df.iloc[subsetindices, j+1].values.tolist()))

        indices=sorted(range(len(averageretList)),reverse=True,key=averageretList.__getitem__)
        newindices=[x+1 for x in indices]
        fundList.append(newindices[0:numOfFunds])

num=0
for i in range(rows-rollingwindow-holdingperiod):
    if i% holdingperiod == 0:
        twoperiodList=[rollingwindow+i,rollingwindow+i+holdingperiod]
        portfolio=df.iloc[twoperiodList,fundList[num]].values.tolist()
        initialValue=initialValue*(1+CalculatePortfolioReturn(portfolio))
        portfolioRet.append(initialValue)
        num=num+1

plt.plot(portfolioRet)
plt.show()
print("Finished")
