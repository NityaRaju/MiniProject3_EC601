# MiniProject3_EC601

# Introduction 
Using data from a Portuguese Bank’s telemarketing campaign which sold Term-Deposits, multiple machine learning algorithms were implemented in order to classify whether or not a given customer would subscribe to a term deposit. The benefits of such a classification include better targeted marketing campaigns and therefore cost reductions as well minimal negative externalities to those that would not like to subscribe to a term deposit. Through data cleaning, feature selection and feature engineering the dataset is developed and run through the algorithms(Support Vector Machines, Decision Trees, Naive Bayes.) We conclude that Naive Bayes works best at this classification task when measured on Accuracy scores,F-scores and Run-times.

# Dataset
The dataset is quite large to load. Here is the link for it:
https://archive.ics.uci.edu/ml/datasets/Bank+Marketing 


The dataset comprizes of 21 features and 41,188 rows(customers), including both categorical and numerical types. The customers in the training data set were classified based on whether or not they subscribed to a term deposit at the
end of the phone call - either a yes tag or no tag. The features of each customer included a number of
social (marital status, education), economic (job, consumer price index) and personal (age)
details. The training data set contained 20 different customer attributes/features plus the
classification of whether or not they signed up for the term deposit. The dataset was subject
to several machine learning techniques to build a data-driven prediction model to predict
the success of bank telemarketing.


 # Model building
The dataset was split into a training set and testing set (70% - 30%). The training set
was used to train a particular model, and then cross-validate the errors to find optimum
parameters.

SVM:
Python provides the package sklearn.svm.SVC. The support vector machine algorithm finds
a hyperplane in an N-dimensional space that distinctly classifies the data points. In addition
to performing linear classification, SVMs can efficiently perform a non-linear classification us-
ing the ‘kernel trick’ and implicitly mapping their inputs into high-dimensional feature spaces.

Naive Bayes:
Python provides the package sklearn.naivebayes.GaussianNB. Naive Bayes classifiers are a
collection of classification algorithms based on Bayes’ Theorem. It is not a single algorithm
but a family of algorithms where all of them share a common principle. It’s relatively simple
to understand and build . A Naive Bayes model is easily trained and is not sensitive to
irrelevant features. It assumes every feature is independent, which isn’t always the case.
Due to the simplicity of the naive assumption, this method was chosen as a benchmark to
compare with other hyper parameterized models.

KNN:
Python provides the package sklearn.neighbors.KNearestClassifier. K-Nearest Neighbors is a
simple algorithm that stores all available cases and classifies new cases based on a similarity
measure and in this instance, it is the Euclidean distance.

# Results
<img src = "https://github.com/NityaRaju/MiniProject3_EC601/blob/master/Screen%20Shot%202019-12-06%20at%203.44.01%20PM.png">

Accuracy
<img src ="https://github.com/NityaRaju/MiniProject3_EC601/blob/master/Screen%20Shot%202019-12-06%20at%203.54.18%20PM.png">

# Special project request

<img src = "https://github.com/NityaRaju/MiniProject3_EC601/blob/master/email.jpg">
