# LKB(c) 2015-16
# supporting scripts

from __future__ import division #so I can have float as std and int as //

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.style.use('ggplot')
import seaborn as sns
import numpy as np
#import scipy
#import copy



############################
# Week 3

#simple user profile algorithm
# count the total the number of positive and negative evaluations associated with each attribute
def userProfile(preferecesData,userVotes):
  cols = [pd.DataFrame(preferecesData[col].values * userVotes.values, columns=[col]) for col in preferecesData]
  votes = cols[0].join(cols[1:])
  votes = votes.sum()

  return votes

#simple user profile algorithm  taking into consideration word frequency as well 
# count the total the number of positive and negative evaluations associated with each attribute

def userProfileWithIDF(preferecesData,userVotes,IDF):
  cols = [pd.DataFrame(preferecesData[col].values * userVotes.values, columns=[col]) for col in preferecesData]
  votes = cols[0].join(cols[1:])
  votes = votes.sum()
  votes = votes*IDFx

  return votes



############################
# Week 4


#find top 5 correlations for the specific user
def GetTopFive(user):
  #user.sort(ascending=False)
  user.sort_values(inplace=True,ascending=False)
  top5 = user.head(6) #get top6
  top5 = top5.tail(-1) #remove 1st - autocorr with itself
  return top5


#nice correlation plot 
# source - internet
def MakeNiceCorrPlot(pandaDF):
  corr = pandaDF.corr()

  # Generate a mask for the upper triangle
  mask = np.zeros_like(corr, dtype=np.bool)
  mask[np.triu_indices_from(mask)] = True
  # Set up the matplotlib figure
  f, ax = plt.subplots(figsize=(11, 9))
  # Draw the heatmap with the mask and correct aspect ratio
  sns.heatmap(corr, mask=mask, cmap="gist_rainbow", vmax=.3,square=True,linewidths=.5, cbar_kws={"shrink": .5}, ax=ax); 
  # xticklabels=5, yticklabels=5, 


  #Create prediction using other user votes using corr between users
# Correlation series (UserID,corrWithTargetUser) Votes(MovieID,Votes)
def UserBasedPrediction(CorrSeries,Votes):

  predictedVotes = pd.Series(0,index=Votes.index)
  totalWeight = predictedVotes[:] #makes a copy of the list
  #CorrSeries.values and #CorrSeries.index.values

  #iterate through corr and relevant userIDs
  for userID,weight in CorrSeries.iteritems():
    #estimate vote from this user, if nan then vote == 0
    predictedVotes = predictedVotes + Votes.ix[:,userID].fillna(value=0)*weight
    #if no vote, weight ==0, hence weight will be diff for each element in the list
    totalWeight = totalWeight + Votes.ix[:,userID].notnull() * weight

  #calculate the final votes
  predictedVotes = predictedVotes/totalWeight
  predictedVotes.replace([np.inf, -np.inf], 0,inplace=True) #in case of div/0

  return predictedVotes


#Create prediction using other user votes using corr between users normalised as difference from average votes
# Correlation matrix (targetUserID,corrWithTargetUser) Votes(MovieID,Votes)
def UserBasedPredictionNromalised(CorrSeries,Votes,targetUserID):
  
  #lets get mean vote for each movie first
  meanUserVotes = Votes.mean(axis=0).fillna(value=0) #mean() autoskip text and NaNs
  predictedVotes = pd.Series(0,index=Votes.index) 
  totalWeight = predictedVotes[:]

  #iterate through corr and relevant userIDs
  for userID,weight in CorrSeries.iteritems():
    #estimate diff between this vote and this users mean; 
    userDiffFromMean = Votes.ix[:,userID] - meanUserVotes[userID] #nan's will remain nan's
    #pdb.set_trace()
    predictedVotes = predictedVotes + userDiffFromMean.fillna(value=0)*weight #nan  == 0
    #if no vote, weight ==0, hence weight will be diff for each element in the list
    totalWeight = totalWeight + Votes.ix[:,userID].notnull() * weight

  #calculate the final votes
  predictedVotes = predictedVotes/totalWeight +  meanUserVotes[targetUserID]
  predictedVotes.replace([np.inf, -np.inf], 0,inplace=True) #in case of div/0

  return predictedVotes


############################
# Week 5

