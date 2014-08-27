library(caret)
library(rpart)
library(rattle)
library(rpart.plot)
library(RColorBrewer)
library(tree)
library(randomForest)
library(e1071)
library(ggplot2)

# Set working directory
setwd("D:\\Datasets\\Ocean Microbes")

# Read the data file
data <- read.csv("seaflow_21min.csv")

# Since there is no single identifier (we have composite of file_id and cell_id), adding an id column
id <- rownames(data)
data <- cbind(id=id, data)

# Create 2 equal partitions of data for training and test
test <- data[sample(1:nrow(data), round(nrow(data)/50), replace="F"),]
train <- subset(data, !(data$id %in% test$id))

# Question 1: How many particles labeled "synecho" are in the file provided?
length(data$id[data$pop == 'synecho'])
# Answered 18146

# Question 2: What is the 3rd Quantile of the field fsc_small?
summary(data$fsc_small)[5]
# Answered 39180

# Question 3: What is the mean of the variable "time" for your training set?
summary(train$time)[4]
# Answered 340

# Question 4: In the plot of pe vs. chl_small, the particles labeled ultra appear to be somewhat "mixed" with which two other populations of particles?
plot(x=data$pe, y=data$chl_small, main="Pe by Pop", col=data$pop, pch=substring(data$pop, 1, 1))
# Answered nano and pico

# Question 5: Use print(model) to inspect your tree. Which populations is your tree incapable of recognizing? (Which populations do not appear on any branch?) Hint: Look
# Welcome to Decision Trees. We'll use Random Partitioning here.
form <- formula(pop ~ fsc_small + fsc_perp + fsc_big + pe + chl_big + chl_small) # This describes a formula for decision tree, where pop is the variable on which tree is constructed
model <- rpart(form, method="class", data) # The data fit (model) will be returned using formula above
print(model)
fancyRpartPlot(model)
# Answered crypto

# Question 6: Most trees will include a node near the root that applies a rule to the pe field, where particles with a value less than some threshold will descend down one branch, and particles with a value greater will descend down a different branch.
# If you look at the plot you created previously, you can verify that the threshold used in the tree is evident visually. What's the threshold on 'pe' field learned?
# Answered 5004 (looking at top branching)

# Question 7: Based on your decision tree, which variables appear to be most important in predicting the class population?
# Answered pe and chl_small

# Question 8: How accurate was your decision tree on the test data? Enter a number between 0 and 1
form <- formula(pop ~ fsc_small + fsc_perp + fsc_big + pe + chl_big + chl_small)
model <- rpart(form, method="class", data=train) # Learn on Training data this time
test$predicted <- predict(model, type="class", test)
print (length(test$pop[test$pop == test$predicted])/nrow(test))
# Answered 0.8500346

# Question 9: How acurate was your random forest model on the test data? Enter a number between 0 and 1
rf_model <- randomForest(form, data=train, importance=TRUE, ntree=20)
test$predicted <- predict(rf_model, test)
print (length(test$pop[test$pop == test$predicted])/nrow(test))
# Answered 0.9225985

# Question 10: Function importance(model) determines which variables appear to be most important in terms of the gini impurity measure. Which ones?
importance(rf_model)[,7]
# Answered pe and chl_small

# Question 11: What was the accuracy of your support vector machine model on the test data? Enter a number between 0 and 1
# Use this for speed test: chunk <- data[sample(1:nrow(data)/10, round(nrow(data)/10), replace="F"),]
svm_model <- svm(form, data=train)
test$predicted <- predict(svm_model, test)
print (length(test$pop[test$pop == test$predicted])/nrow(test))
# Answered 0.926745

# Question 12: Construct a confusion matrix for each of the three methods using the table function. What appears to be the most common error the models make?
table(pred=test$predicted, true=test$pop)
# Answered "ultra" is mistaken for "nano"

# Question 13: The variables in the dataset were assumed to be continuous, but one of them takes on only a few discrete values. Which variable?
unique(data$fsc_big) # Has only 6 values as compared to chl_big, pe, fsc_perp, chl_small and fsc_small
# Answered fsc_big

# Question 14: After removing data associated with file_id 208, what was the effect on the accuracy of your svm model? Enter a positive or negative number representing the net change in accuracy, where a positive number represents an improvement in accuracy and a negative number represents a decrease in accuracy.
new_data <- subset(data, data$file_id != 203)
new_test <- new_data[sample(1:nrow(new_data), round(nrow(new_data)/50), replace="F"),]
new_train <- subset(new_data, !(new_data$id %in% new_test$id))
svm_model <- svm(form, data=new_train)
new_test$predicted <- predict(svm_model, new_test)
print (length(new_test$pop[new_test$pop == new_test$predicted])/nrow(new_test))
# Answered 0.0492285