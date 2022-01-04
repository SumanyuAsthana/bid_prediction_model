import sys
sys.path.append('/content/gdrive/MyDrive/freelancer-narender-s-261121/qlearning FINAL 5')
from agent import agent
from dataPrep2 import *
class env():
  # This is our environment
  # Our environment has one random forest classifier that acts as the actor/agent here
  # In our environment we send data containing campaign ids and dates and several keywords that can be bought under that campaignId on that date
  # We need to train the random forest classifier to wether or not to place a bid on each row of the entire data given to us


  #usepca is for using or not using pca
  def __init__(self,usePca=False,pcac=5,n_estimators=200,columns=['keywordId','campaignId','tAcos','price','hour','month','day']):
    self.columns=columns
    #we define our agent in another file look at the top its imported
    self.model=agent(n_estimators=n_estimators,usePca=usePca,pcac=pcac)
  def train(self,data,verbose=2,epochs=2,stdz=False):
    # when we are given data we need to first wether in truth we should bid for each row or not
    # Only when we do so can we start training the model 
    # To find the correct bids we use knapsack algorithm
    # This knapsack algorithm acts as our critic also 
    # It is implemented in the function dataMod which is in the fule dataPrep2 
    data2=dataMod(data)
    #we use X which is given by the data below:
    X=data2[
      self.columns
    ]
    #to predict the correct bids:
    Y=data2['correctBid'].values
    self.model.train(X,Y,verbose=verbose,epochs=epochs,stdz=stdz)
  def test(self,data,showPer=False,stdz=False):
    #in the arguments above we have showPer which stands for showPerformance
    #if this is true then we will get metrices and comparisons for our prediction vs the correct values 
    if 'sales' in data.columns and 'price' in data.columns and showPer==True:
      #here showPer is given true so we need to find the correct bids using the datMod function as we had used for training
      #then once we have the correct bids we can make comparison with our predictions as well
      data=dataMod(data)
      X=data[
        self.columns
      ]
      Y_test=data['correctBid'].values
      #we send all the info to our agent to do all the prediction and analysis
      Y_pred=self.model.predict(X,Y_test,showPer,stdz=stdz)
      return Y_pred
    else:
      #here since we dont have to show any performance we don't call the dataMod function
      X=data[
        self.columns
      ]
      Y_pred=self.model.predict(X,stdz=stdz)
      return Y_pred
