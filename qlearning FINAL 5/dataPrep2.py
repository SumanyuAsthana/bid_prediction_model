import sys
sys.path.append('/content/gdrive/MyDrive/freelancer-narender-s-261121/qlearning FINAL 5')
from util import Util
import numpy as np
import pandas as pd
pd.options.mode.chained_assignment = None
#the entire algorithm below can be seen at:
#https://www.geeksforgeeks.org/printing-items-01-knapsack/
#we are simply doing the following in here:
#we get costs profits and the total budget we can use 
#we try to pick those elements that give us the maximum total profit while our sum of costs does not exceen the budget
def getCorrectBids(wt, val,acos, W,T):#costs,profits,budget
  n=len(wt)
  wt=[int(w*100) for w in wt]
  val=[int(w*100) for w in val]
  acos=[int(w*100) for w in acos]
  W=int(W*100)
  T=int(T*100)
  K =[[[0 for t in range(T + 1)] for w in range(W + 1)] for i in range(n + 1)]
  # Build table K[][] in bottom
  # up manner
  for i in range(n + 1):
    for w in range(W + 1):
      for t in range(T+1):
        if i == 0 or w == 0 or t==0:
          K[i][w][t] = 0
        elif wt[i - 1] <= w and acos[i-1]<=t:
          K[i][w][t] = max(val[i - 1]+K[i-1][w-wt[i-1]][t-acos[i-1]] ,K[i - 1][w][t])
        else:
          K[i][w][t] = K[i - 1][w][t]

  # stores the result of Knapsack
  res = K[n][W][T]
  used=[0]*(n)     
  w = W
  t=T
  for i in range(n, 0, -1):
    if res <= 0:
      break
    # either the result comes from the
    # top (K[i-1][w][t]) or from (val[i-1]
    # + K[i-1] [w-wt[i-1]][t-acos[i-1]]) as in Knapsack
    # table. If it comes from the latter
    # one/ it means the item is included.
    if res == K[i - 1][w][t]:
      continue
    else:

      # This item is included.
      # print(wt[i - 1])
      used[i-1]=1
      # Since this weight is included
      # its value is deducted
      res = res - val[i - 1]
      w = w - wt[i - 1]
      t = t - acos[i - 1]
  # wt=[float(w/100) for w in wt]
  # acos=[float(w/100) for w in acos]
  return used
def toPlace(row):
  if (row['profit'])>0:
    return 1
  return 0
def getProfit(row):
  #this function finds for each row the profit that can be generated
  return max(0,(row['sales']*row['price']-row['cost']))
def getAcos(row):
  if row['cost']==0:
    return 0
  elif (row['sales']*row['price'])==0:
    return 10000
  return row['cost']/(row['sales']*row['price'])
def dataMod(Data):
  #this is the function which we use to fill up the database with the correctBid values
  
  #we will use below list to mantain all the data for particular campaigns and particular days
  dList=list()
  for cid in range(13):
    for day in range(367):
      #WE HAVE TO GO TO A CERTAIN CAMPAIGN ID AND A CERTAIN DAY TO RUN THE KNAPSACK ALGO THAT 
      #WOULD FILL UP BID CHOICE 0/1
      if day%100==0:
        print(cid,'  ',day)
      #choose all the data for that campaignId and that day
      data=Data[(Data['campaignId']==cid)&(Data['dayVal']==day)]
      if len(data)==0:
        continue
      #find the profits for that data
      data['profit']=data.apply(lambda row:getProfit(row),axis=1)
      data['acos']=data.apply(lambda row:getAcos(row),axis=1)
      maxCostPoss=np.sum(data[(data['profit']>0)]['cost'].values)
      maxAcosPoss=np.sum(data[(data['profit']>0)]['acos'].values)
      data['correctBid']=0
      givenBudget=np.min(data['campaignBudget'].values)
      givenTacos=np.min(data['tAcos'].values)
      if maxCostPoss<=givenBudget and maxAcosPoss<=givenTacos:
        data['correctBid']=data.apply(lambda row:toPlace(row),axis=1)
      else:
        data['correctBid']=getCorrectBids(data['cost'].values,data['profit'].values,data['acos'].values,givenBudget,givenTacos)
      
      #add the data to the list
      dList.append(data)
  #convert list to dataframe and send
  result = pd.concat(dList)
  del dList
  return result




