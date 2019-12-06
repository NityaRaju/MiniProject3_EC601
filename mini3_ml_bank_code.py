# -*- coding: utf-8 -*-
"""Mini3 ML_Bank_code.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1aNjQLTfnbuVjK2CDWyzpYp5NJoNhq7Qo

# Portuguese Bank Marketing - Machine Learning

The data is associated with the direct marketing campaigns (phone calls) of a Portuguese banking institution. The classification goal is to predict if the client will subscribe to a term deposit. The outcome of this classification can enable marketing teams to more accurately predict customer bases and therefore cut down on costs.
"""

# Commented out IPython magic to ensure Python compatibility.
####################################################################################################################
#Importing relevant packages

import seaborn as sns
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import pandas as pd
import sklearn.linear_model as linear
import random
sns.set(style="darkgrid")
plt.style.use('ggplot')
# %matplotlib inline
from sklearn.model_selection import ShuffleSplit
from sklearn.model_selection import train_test_split
from sklearn import metrics as mt
import datetime
import time
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_curve, auc

"""# Loading the Dataset

The dataset comprizes of 21 features and 41,188 rows, including both categorical and numerical types.
"""

dataframe = pd.read_csv( "bank-additional-full.csv", sep=";")
dataframe.head()

dataframe.describe()

"""# Data Cleaning and Exploration

The data itself needs very little cleaning. It has no null or NaN values. However, other features need to be adjusted. The feature 'pdays' indicates time elasped from the last contact attempt. If no contact was priorly made, we assigned 'pdays' value of 0 instead of 999
"""

dataframe.isnull().sum()

dataframe['pdays'].replace(999,0, inplace = True)

## data exploration-value counting each feature to perform feature selection
object_list = []
number_list = []

def examine_data_frame( df):
    for name in df.columns:
        print ("----------")
        print (df[ name].dtype)
        if df[ name].dtype is np.dtype( 'O'):
            print (df[ name].value_counts())
            print ("Name: ", name)
        else:
            print (df[ name].describe())

examine_data_frame(dataframe)

"""The feature 'education' comprises of 8 categories, including; 'basic.9y', 'basic.6y' and 'basic.9y'. In order to reduce the number of eventual features and the dimensionality of our model, we combine these into a single category; 'basic'."""

dataframe.replace(['basic.6y','basic.4y', 'basic.9y'], 'basic', inplace = True)

"""## Feature Selection

Exploring the data suggests that we drop some features.The feature 'default' which indicates whether or not the individual has credit in default. Since there were only three individuals that had defaulted, we remove those observations from the dataset. 'Duration' is also dropped as it is only included in the dataset as a benchmark variable. Furthermore, one only knows the 'duration' of the telemarketing call after the fact so it is not a relevant variable.
"""

##feature selection
dataframe['duration'].value_counts() 
dataframe.drop(['duration'], inplace = True, axis=1)

dataframe['default'].value_counts()
dataframe.drop(['default'], inplace = True, axis=1)

"""# Data Visualization

This section picks features that we hypothesize to be important for the model. We pick these features intuitively and observe their distribution across the data through visualizations.
"""

frequencies = pd.crosstab(dataframe["marital"], dataframe[ "y"]).apply(lambda r: r/len(dataframe))
print (frequencies)

sns.heatmap( frequencies,cmap = 'viridis')

dataframe['age'].hist()
plt.title("Distribution of Age")
plt.xlabel("Age")
plt.ylabel("Frequency")

dataframe['cons.conf.idx'].hist()
plt.title("Distribution of Consumer Confidence")
plt.xlabel("Consumer Confidence Index")
plt.ylabel("Frequency")

dataframe['euribor3m'].hist()
plt.title("Distribution of 3-month Euribor Rate")
plt.xlabel("Euribor rate")
plt.ylabel("Frequency")

"""# Feature Engineering and Final Data Cleaning

We then engineer new features by conducting a 'One-hot encoding' on all the categorical features in our dataset to convert them to numerical values. Furthermore, we normalize the data and this is the final step in cleaning our features.
"""

from sklearn.preprocessing import StandardScaler

numbers = ['age',
 'campaign',
 'pdays',
 'previous',
 'emp.var.rate',
 'cons.price.idx',
 'cons.conf.idx',
 'euribor3m','nr.employed']

obj_ss = StandardScaler()
vals = obj_ss.fit_transform(dataframe[numbers])
dataframe[numbers] = vals

dfo = pd.get_dummies(dataframe[dataframe.columns[:-1]])
dfo['y'] = dataframe['y']
dfo['y'] = dfo['y'].apply(lambda x: 1 if x =='yes' else 0)

dfo.shape

"""Seperating the Data into Training and Testing Sets"""

X = dfo.iloc[:,:-1]
y = dfo[dfo.columns[-1]]

>>> X_train, X_test, y_train, y_test = train_test_split(
...     X, y, test_size=0.33, random_state=42)

"""Conducting PCA analysis to aid with feature selection"""

from sklearn.decomposition import PCA

pca = PCA(n_components=2)
two_components = pca.fit_transform(X)
df_pca = pd.DataFrame(data = two_components
             , columns = ['principal component 1', 'principal component 2'])
df_pca['y'] = dfo['y'].values

sns.set()
sns.set_palette('Set1')
fig = plt.figure(figsize=(10,12))
sns.lmplot( x = 'principal component 1', y = 'principal component 2', hue = 'y', data = df_pca, fit_reg= False )
fig = plt.gcf()
fig.savefig('PCA.png',bbox_inches='tight' )

# Commented out IPython magic to ensure Python compatibility.
import numpy as np
from sklearn.decomposition import PCA
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import scale
# %matplotlib inline


pca = PCA(n_components=57)

pca.fit(dfo)

#The amount of variance that each PC explains
var= pca.explained_variance_ratio_

#Cumulative Variance explains
    
var1 =np.cumsum(np.round(pca.explained_variance_ratio_, decimals=4)*100)
print(var1)

plt.plot(var1)
plt.title("PCA Analysis")
plt.xlabel("PC component")
plt.ylabel("Cumulative Variation Explained")

"""# Defining the Models"""

# computational libraries
import numpy as np
import pandas as pd

import pickle

#Visualization Metrics
import matplotlib.pyplot as plt
import seaborn as sns 
from sklearn.model_selection import validation_curve, learning_curve

#Classification Algorithms
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier

import sklearn

#Metrics
from sklearn.metrics import accuracy_score, fbeta_score, classification_report, make_scorer, f1_score




from time import time


#Pipeline to run and test multiple ML algorithms
def train_predict(learner, X_train, y_train, X_test, y_test): 
    '''
    inputs:
       - learner: the learning algorithm to be trained and predicted on
       - X_train: features training set
       - y_train: income training set
       - X_test: features testing set
       - y_test: income testing set
       
       outputs: dict['train_time', 'pred_time', 'acc_test', 'f_test']
    '''
    results = {}
    
    # Fit the learner to the training data using slicing with 'sample_size'
    start = time() # Get start time
    learner.fit(X_train, y_train)
    end = time() # Get end time
    
    # Calculate the training time
    results['train_time'] = end - start
        
    # Get the predictions on the test set,  
    start = time() # Get start time
    predictions = learner.predict(X_test)
    end = time() # Get end time
    
    #Classification Report
    
    # Calculate the total prediction time
    results['pred_time'] = end - start
        
    # Compute accuracy on test set
    results['acc_test'] = accuracy_score(y_test, predictions)
    
    # Compute F-score on the test set. We use previous beta
    results['f_test'] = f1_score(y_test, predictions, labels=None,
    pos_label=1,
    average='weighted',
    sample_weight=None,

)
    
    report = classification_report(y_test,predictions)
       
        
    # Return the results
    return results, report

def complexity_curve(X_train, y_train, model, hyperparameter, param_range):
    
    from sklearn.metrics import fbeta_score, make_scorer
    
    #score = make_scorer(fbeta_score(y_train,2))
    
    
    
    '''Plot the complexity and learning curves for the model selected'''

    
    train_scores, test_scores = validation_curve( model, X_train, y_train, 
                                                 param_name=hyperparameter, param_range=param_range,
                                                 cv=5, scoring= 'accuracy', n_jobs=1)
    
    # Calculate mean and standard deviation for training set scores
    train_mean = np.mean(train_scores, axis=1)
    train_std = np.std(train_scores, axis=1)

    # Calculate mean and standard deviation for test set scores
    test_mean = np.mean(test_scores, axis=1)
    test_std = np.std(test_scores, axis=1)

   
    #fig = plt.figure(figsize=(10,12))
    sns.set()
    # Plot mean accuracy scores for training and test sets
    plt.plot(param_range, train_mean, label="Training score", color="red")
    plt.plot(param_range, test_mean, label="Cross-validation score", color="g")

    # Plot accurancy bands for training and test sets
    plt.fill_between(param_range, train_mean - train_std, train_mean + train_std, color="lightcoral")
    plt.fill_between(param_range, test_mean - test_std, test_mean + test_std, color="lightgreen")

    # Create plot
    plt.title("Validation Curve")
    plt.xlabel(hyperparameter)
    plt.ylabel("Accuracy Score")
    plt.tight_layout()
    plt.legend(loc="best")
   

    fig = plt.gcf()
    fig.savefig('complexity.png',bbox_inches='tight')
    
    plt.show()
    
def learning_curve_(X_train, y_train, model):


    
    train_sizes, train_scores, test_scores = learning_curve(model,
                                                            X_train, y_train,cv=5, scoring='f1_score',
                                                            n_jobs=-1)
# Number of folds in cross-validation
# Evaluation metric
# Use all computer cores

# 50 different sizes of the training set


    # Create means and standard deviations of training set scores
    train_mean = np.mean(train_scores, axis=1)
    train_std = np.std(train_scores, axis=1)

    # Create means and standard deviations of test set scores
    test_mean = np.mean(test_scores, axis=1)
    test_std = np.std(test_scores, axis=1)
    
    #fig = plt.figure(figsize=(10,12))
    sns.set()

    # Draw lines
    plt.plot(train_sizes, train_mean, color="red",  label="Training score")
    plt.plot(train_sizes, test_mean, color="g", label="Cross-validation score")

    # Draw bands
    plt.fill_between(train_sizes, train_mean - train_std, train_mean + train_std, color="lightcoral")
    plt.fill_between(train_sizes, test_mean - test_std, test_mean + test_std, color="lightgreen")

    # Create plot
    plt.title("Learning Curve")
    plt.xlabel("Training Set Size"), plt.ylabel("Accuracy Score"), plt.legend(loc="best")
    
    
    
    fig = plt.gcf()
    fig.savefig('learning_curve.png',bbox_inches='tight' )
    
    plt.tight_layout()
    plt.show()
    
    
    ################################

model_svm = SVC()
model_NB = GaussianNB()
model_KNN = KNeighborsClassifier(n_neighbors= 7)


results_svm, report_svm = train_predict(model_svm, X_train, y_train, X_test, y_test)
results_NB, report_NB = train_predict(model_NB, X_train, y_train, X_test, y_test)
results_KNN, report_KNN = train_predict(model_KNN, X_train, y_train, X_test, y_test)


results_svm = list(results_svm.values())
results_NB = list(results_NB.values())
results_KNN =  list(results_KNN.values())


results = np.vstack((results_svm,results_NB,results_KNN)
df_results = pd.DataFrame(results,columns = ['train_time', 'pred_time', 'acc_test', 'f_test'], 
                          index = ['SVM', 'NB', 'KNN'])

df_results_table = df_results.copy()

df_results

"""Computing Accuracies"""

#Accuracy

objects = ('SVM', 'NB', 'KNN')
y_pos = np.arange(len(objects))
performance = df_results['acc_test'].values

#fig = plt.figure(figsize=(10,12)
plt.bar(y_pos, performance, align='center',color=['red', 'green', 'blue', 'cyan', 'yellow'], 
        alpha= 0.7, edgecolor='black')
plt.xticks(y_pos, objects)
plt.ylabel('Accuracy')
plt.title('Model Accuracy')
fig = plt.gcf()
fig.savefig('accuracy.png',bbox_inches='tight' )

print('\n', report_NB)

print('\n'+report_KNN)

print('\n'+classification_report(y_test,gpred))