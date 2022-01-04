from datetime import datetime
import numpy as np
import pandas as pd
class Util():
  def fillDates(X):
    # '''This function simply adds rows 'date',"year","month" and "dayVal" to the dataset'''
    X["date"] = pd.to_datetime(X["reportDate"]).dt.date
    #This is the date in string format it is created by using pd.to_datetime
    X["year"] = pd.DatetimeIndex(X['date']).year
    #This is the year of the particular date 
    X["month"] = pd.DatetimeIndex(X['date']).month
    X["day"] = pd.DatetimeIndex(X['date']).day
    def getDayVal(row):
      '''
      this function is given a row in a dataset and it uses a datetime python library
      to get which day of the year is particularly being refered to
      Example 2021-01-02 is the 2nd day so it gives 2 as the result
      '''
      year,month,day=row['year'],row['month'],row['day']
      t = datetime(year,month,day)
      return t.timetuple()[7]
    X["dayVal"]=X.apply(lambda row:getDayVal(row),axis=1)#apply the function to each row
  def convertToCat(df,cols):
    '''
    Column names are given in an array 
    These column contain big numerical data but very few unique values
    This function converts big numerical values to integers
    Say that the campaignId column has 22389123,328491003,633450 as the only unique values in the column
    Then we map 22389123->0,328491003->1,633450->2
    '''
    def getCat(x,d):
      '''We use this function to do the above
      Here we use a dictionary to map big numbers to integers
      If new number is seen we add to dictionary and map to dict length
      '''
      if x not in d:
        d[x]=len(d)
      return d[x] 
    for col in cols:
      dic=dict()
      df[col]=df[col].apply(lambda x:getCat(x,d=dic))
    return df