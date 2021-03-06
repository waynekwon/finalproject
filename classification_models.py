import numpy as np
import pandas as pd

from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.cross_validation import train_test_split
from sklearn import metrics
from sklearn.tree import DecisionTreeClassifier
from clean_data import get_clean_data

file_n = 'movie_metadata.csv'
mydata=get_clean_data(file_n)

#--------------- PREPARING FOR CLASSIFICATION MODELS ---------------



#storing the resopnse variable in 'response' for easier code writing
response = mydata['movie_response']

#create a list of predictors to include in classification model
predictor_list = ['title_year', 'director_facebook_likes', 'actor_3_facebook_likes', 'actor_1_facebook_likes', 'facenumber_in_poster', 'content_rating', 'budget', 'actor_2_facebook_likes',
'Action','Adventure', 'Animation', 'Biography', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Family', 'Fantasy', 'History', 'Horror', 'Music', 'Musical', 'Mystery', 'News', 'Romance', 'Sci-Fi', 'Short','Sport', 'Thriller','War', 'Western' ]
movie_features = mydata[predictor_list]

#transform X from pandas dataframe to numpy arrays
X = movie_features.as_matrix()
#transform y from pandas to 1D list
y = list(mydata['movie_response'].values)


#--------------- SPLITTING INTO TRAINING & TESTING SETS ---------------

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2)#, random_state = 2) #to keep splitting constant, set 'random_state=1'
#print X_train.shape, X_test.shape
#print len(y_train), len(y_test)


#--------------- CARRY OUT CLASSIFICATION MODELS ---------------

#call in the models
logreg = LogisticRegression()
knn2 = KNeighborsClassifier(n_neighbors=15) # K=15
knn3 = KNeighborsClassifier(n_neighbors=20) # K=20
dec_tree = DecisionTreeClassifier()

#fit the model with training set
logreg.fit(X_train, y_train)
knn2.fit(X_train, y_train)
knn3.fit(X_train, y_train)
dec_tree.fit(X_train, y_train)

#make predictions on the testing set
log_y_pred = logreg.predict(X_test)
knn2_y_pred = knn2.predict(X_test)
knn3_y_pred = knn3.predict(X_test)
dec_tree_y_pred = dec_tree.predict(X_test)

#compare actual response values with predicted values
log_accuracy = metrics.accuracy_score(y_test, log_y_pred)
knn2_accuracy = metrics.accuracy_score(y_test, knn2_y_pred)
knn3_accuracy = metrics.accuracy_score(y_test, knn3_y_pred)
dec_tree_accuracy = metrics.accuracy_score(y_test, dec_tree_y_pred)
print "Logitstic Accuracy: ", log_accuracy
print "KNN (K=15) Accuracy: ", knn2_accuracy
print "KNN (K=20) Accuracy: ", knn3_accuracy
print "Decision Tree Accuracy: ", dec_tree_accuracy

#FOR K-NN: find the best value of k by iterating its value
k_range = range(1,25)
scores = []
for k in k_range:
    knn = KNeighborsClassifier(n_neighbors = k)
    knn.fit(X_train, y_train)
    y_pred = knn.predict(X_test)
    scores.append(metrics.accuracy_score(y_test, y_pred))

#if you want to predict using out-of-sample observation
#knn.predict(["put in the value for each column, or predictors, as a list" ])


#--------------- GRAPH K-NEAREST NEIGHBORS ---------------

import matplotlib.pyplot as plt

plt.plot(k_range, scores)
plt.xlabel('Value of K for KNN')
plt.ylabel('Testing Accuracy')

plt.show()
