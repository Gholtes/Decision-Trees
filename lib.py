import pandas as pd
import numpy as np
from sklearn import tree
import graphviz #for visulization of the fitted tree

raw = pd.read_csv("golf.csv")

#Get dummy variables for each column in the datafile
for var in ['Outlook', 'Temperature', 'Humidity', 'Windy']:
    dummy = pd.get_dummies(raw[var])
    #Drop first column to avoid dummy variable trap
    var_to_drop = list(dummy)[0]
    dummy.drop([var_to_drop], inplace=True, axis=1)
    #add to DataFrame named 'processed'
    try:
        processed = pd.concat([processed, dummy], axis=1)
    except NameError:
        processed = dummy

#Convert data to array to be fed to sklearn
Y = np.array(raw["Y"])
X = np.array(processed)

#Fit the model
clf = tree.DecisionTreeClassifier()
clf = clf.fit(X, Y)

#Get predicted values from the training set
predictions = clf.predict(X)
confusion_matrix = [[0,0],[0,0]]
key = {"yes":0, "no":1}
for i in range(len(predictions)):
    confusion_matrix[key[predictions[i]]][key[Y[i]]] += 1

#display confusion matrix
print(confusion_matrix[0])
print(confusion_matrix[1])

#Render the tree
variable_names = list(processed)
dot_data = tree.export_graphviz(clf,
                                feature_names = variable_names,
                                class_names = ["yes", "no"],
                                out_file=None)
graph = graphviz.Source(dot_data)
graph.render("golf_lib")
