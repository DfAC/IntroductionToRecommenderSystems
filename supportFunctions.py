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
  return top5.round(3)


#nice correlation plot, in- correlationMatrix
# source - https://stanford.edu/~mwaskom/software/seaborn/examples/many_pairwise_correlations.html
def MakeNiceCorrPlot(corrMatrix):
  #corrMatrix = pandaDF.corr()

  # Generate a mask for the upper triangle
  mask = np.zeros_like(corrMatrix, dtype=np.bool)
  mask[np.triu_indices_from(mask)] = True
  # Set up the matplotlib figure
  f, ax = plt.subplots(figsize=(11, 9))
  # Draw the heatmap with the mask and correct aspect ratio
#"gist_rainbow"
  correlation_cmap = sns.diverging_palette(10, 200,center='light', as_cmap=True)
  sns.heatmap(corrMatrix, mask=mask, cmap=correlation_cmap, vmax=.3,square=True,linewidths=.5, cbar_kws={"shrink": .5}, ax=ax,xticklabels=5); 
  # xticklabels=5, yticklabels=5, 



# Create prediction using other user votes using corr between users
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
# Week 6

def getCosineCorrMatrix(pandaDF):

  # get inner prodict of all columns in nice corr matrix
  dataArray = pandaDF.fillna(0).values.astype('float') #convert to numpy, float for adjusted values
  numerator = np.einsum('ij,ik', dataArray, dataArray)
  #convert euclidean L2 norms to matrix
  L2norm = np.sqrt(np.square(pandaDF.transpose()).sum(axis=1))
  denominator = np.einsum('i,j', L2norm, L2norm)

  #get our corr matrix -> sim(i,j)
  corrMatrix = pd.DataFrame(numerator/denominator,columns=pandaDF.columns, index=pandaDF.columns)
  
  #visualise this
  MakeNiceCorrPlot(corrMatrix)

  #return matrix
  return corrMatrix
######################################################
# my other attempts
# #http://stackoverflow.com/questions/21467429/pairwise-matrix-from-a-pandas-dataframe
# #first approach - write it yourself
# dataArray = dfData.fillna(0).values.astype('int') #for numpy
# result = pd.DataFrame(np.einsum('ij,ik', dataArray, dataArray),columns=dfData.columns, index=dfData.columns)
# #second - slower one
# df2 = dfData.applymap(lambda x: int((not pd.isnull(x)))) 
# result2 = df2.T.dot(df2)


# # this is not working either
# #sci kit approach
# from sklearn.metrics.pairwise import pairwise_distances

# dataArray = dfData.fillna(0).values.astype('int') #for numpy
# corrMatrix = pairwise_distances(dataArray,metric='cosine',n_jobs=1) #=1 for production code, 1 for debugging
# #l2matrix = pairwise_distances(dataArray,metric='l2',n_jobs=1) #=1 for production code, 1 for debugging 
# result = 1-pd.DataFrame(corrMatrix,columns=dfData.columns, index=dfData.columns) #from distance to correlation

# from scipy.spatial.distance import cosine

# data = dfData.fillna(0)
# 1- cosine(data.ix[:,0],data.ix[:,1])
##############################################################



# calculate prediction for specific user (defined by his voting) and correlation matrix of items
# in: userVotesMatrix, allItemVotesMatrix
# out: correlation matrix 
# why do we go via numpy array? use Pandas when you need alignment or grouping by index, use NumPy when doing computation on N-dimensional arrays

def ItemBasedPrediction(userRatings,corrMatrix):

  #only consider non-negative correlations
  corrMatrix = corrMatrix[corrMatrix>0]  

  # find correlation betwen user votes and other items
  arrayUser = userRatings.fillna(0).values.astype('float') #convert to numpy, float for adjusted values
  arrayItem = corrMatrix.fillna(0).values.astype('float')
  #dot product, same as arrayUser.dot(arrayItem) if 'ij, jk->ik'
  predictedVotes = np.einsum('ij, jk->ki', arrayUser,arrayItem) #rotated output matrix

  arrayUser = userRatings.notnull().values.astype('float') #convert to numpy, float for adjusted values
  totalWeight = np.einsum('ij, jk->ki', arrayUser,arrayItem) #rotated output matrix

  predictedVotes = pd.DataFrame(predictedVotes/totalWeight,index=corrMatrix.columns,columns=userRatings.index) 
  #predictedVotes.replace([np.inf, -np.inf], 0,inplace=True) #in case of div/0

  return predictedVotes



# find top 5 Predictions for the specific user using item prediction
# note that this is diff from the week4 implementation
def GetTopFivePredictions(predictedVotes):
  #user.sort(ascending=False)
  predictedVotes = predictedVotes.iloc[:,0].copy() #just get series
  predictedVotes.sort_values(inplace=True,ascending=False)

  return predictedVotes.head(5).round(3)





  ############################
# Week 7