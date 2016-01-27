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

#simple user profile algorythm - 
# count the total the number of positive and negative evaluations associated with each attribute
def userProfile(preferecesData,userVotes):
  cols = [pd.DataFrame(preferecesData[col].values * userVotes.values, columns=[col]) for col in preferecesData]
  votes = cols[0].join(cols[1:])
  votes = votes.sum()

  return votes

#simple user profile algorythm  taking into consideration word frequency as well 
# count the total the number of positive and negative evaluations associated with each attribute

def userProfileWithIDF(preferecesData,userVotes,IDF):
  cols = [pd.DataFrame(preferecesData[col].values * userVotes.values, columns=[col]) for col in preferecesData]
  votes = cols[0].join(cols[1:])
  votes = votes.sum()
  votes = votes*IDF

  return votes

############################
# Week 4


#find top 5 correlations for the specific user
def GetTopFive(user):
    user.sort(ascending=False)
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