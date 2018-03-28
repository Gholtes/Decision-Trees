library("rpart", "rpart.plot")

#Read data
data <- read.csv("titanic.csv")
#Separate into mutually exclusive training and testing sets.
bound <- floor((nrow(data)/4)*3)       #75% training data
df <- data[sample(nrow(data)), ]       #sample rows 
df.train <- df[1:bound, ]              #get training set
df.test <- df[(bound+1):nrow(df), ]    #get test set

#Determine the best cp to use
min_RMSE = 9999    # ~inf
Best_CP = 0.01     #Default
CPS = c(0.1, 0.01, 0.001, 0.0001, 0.00001, 0.000001, -1)

for (CP in CPS) {
  #Fit tree on train data
  dectree <- rpart(Y ~ Pclass + Sex + Embarked + SibSp + Parch,
                   data = df.train, 
                   method = "class",
                   control = rpart.control(cp = CP),
                   parms = list(split = "information"))
 
  #get fitted values from test data
  fitted <- data.frame(predict(dectree, df.test, type = "prob"))
  prob_1 = fitted$X1
  #Evaluate loss
  RMSE = mean((prob_1 - df.test$Y)^2)
  
  if (RMSE < min_RMSE) {
    min_RMSE = RMSE
    Best_CP = CP
  }
}


#fit the tree with Best_CP from before
dectree <- rpart(Y ~ Pclass + Sex + Embarked + SibSp + Parch,
            data = data, 
            method = "class",
            control = rpart.control(cp = Best_CP),
            parms = list(split = "information")
            )

#Get predicted values from whole dataset
fitted <- data.frame(predict(dectree, train, type = "prob"))
fitted$prediction <- data.frame(predict(dectree, train, type = "class"))

#Render the tree
rpart.plot(dectree)
