#this is where we build our agent
import matplotlib.pyplot as plt
import gc
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix,f1_score,precision_score,recall_score,accuracy_score
import tensorflow as tf
import numpy as np
import random
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense,Dropout
from reward import *
class agent:
  #we start by defining a model for the agent
  def __init__(self,model=None,n_estimators=200,usePca=False,pcac=5):
    self.model=model
    #we can use a previously trained randomForest or a new one 
    if model==None:
      self.model=RandomForestClassifier(n_estimators=n_estimators,verbose=2,n_jobs=-1)
    self.usePca=usePca#using pca or not
    self.pcac=pcac
    if usePca==True:
      self.pca=PCA(n_components=pcac)
  def train(self,x,y,verbose=2,epochs=3,stdz=False):
    #if we specify stdz=True then we standardize the entire X before beginning training
    if stdz==True:
      x=(x-x.mean())/x.std()
    if self.usePca==True:
      x=self.pca.fit_transform(x)
    self.model.fit(x,y)
  def Rand(self,start, end, num):
    #this is a utility function that give num random numbers between start and end all unique
    return random.sample(range(start,end),num)
  def predict(self,x,Y_test=None,showPer=False,stdz=False,bPrec=1):
    #if we specify stdz=True then we standardize the entire X before beginning training
    if stdz==True:
      x=(x-x.mean())/x.std()
    #then predict the results using the agent
    if self.usePca==True:
      x=self.pca.fit_transform(x)
    Y_pred=self.model.predict(x)
    if showPer==True and Y_test is not None:
      #since we are asked to show performance we lay out the following metrices:
      print("confusion_matrix:")
      print(confusion_matrix(Y_test, Y_pred))
      print("precision_score:")
      print(precision_score(Y_test, Y_pred))
      print("recall_score:")
      print(recall_score(Y_test, Y_pred))
      print("accuracy_score:")
      print(accuracy_score(Y_test, Y_pred))
      print("f1_score:")
      print(f1_score(Y_test, Y_pred))
    return Y_pred
  
  