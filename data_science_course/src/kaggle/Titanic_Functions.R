library(rattle)
library(rpart.plot)
library(RColorBrewer)
library(rpart)
library(randomForest)

data_file <- "test.csv"
view_process <- FALSE
output_file <- "mygenderageclassmodel_R.csv"

analyze <- function(data_file, output_file="mymodel.csv", view_process=FALSE)
{
    # Read the training data
    dataset <- read.csv(data_file)    
    # Fetch distribution of survivors
    print (table(dataset$Survived))
    
    # IMPORTANT: This will distribute the dataset of survivors gender-wise, by dividing cells with row totals, instead of total number
    if (view_process)
    {
        print (prop.table(table(dataset$Sex, dataset$Survived), 1))
    }
    
    # Fill in missing values with average age
    bad <- is.na(dataset$Age)
    dataset$Age[bad] <- round(mean(dataset$Age[!bad]))
    
    # Add 3 columns to dataseting datasetset, determining if they are Child, Schooler, Teen, Young or Old
    dataset$AgeGroup <- "X"
    dataset$AgeGroup[dataset$Age < 6] <- "Child"
    dataset$AgeGroup[dataset$Age >= 6 & dataset$Age < 13] <- "Schooler"
    dataset$AgeGroup[dataset$Age >= 13 & dataset$Age < 20] <- "Teen"
    dataset$AgeGroup[dataset$Age >= 20 & dataset$Age < 40] <- "Young"
    dataset$AgeGroup[dataset$Age >= 40] <- "Old"
    # IMPORTANT: This will aggregate dataseting dataset based on both AgeGroup and Sex columns, (like group by AgeGroup, Sex in SQL). The aggregate function will be sum/length
    if(view_process)
    {
        print (aggregate(Survived ~ AgeGroup + Sex, dataset, FUN=function(x) {sum(x)/length(x)}))
        # These indicted that passengers of Age group "Child" have better chance of survival
    }
    
    # Fill in missing values with average fare
    bad <- is.na(dataset$Fare)
    dataset$Fare[bad] <- round(mean(dataset$Fare[!bad]))
    
    # Use Kmeans algorithm to identify 3 clusters of fare
    km <- kmeans(dataset$Fare, 3)
    fares <- sort(km$centers)
    
    # Add a column to dataseting datasetset, changing quantitative data fore "fare" into qualitative, using centers from k-means
    dataset$FareGroup <- 'X'
    dataset$FareGroup[dataset$Fare < fares[1]] <- 'L'
    dataset$FareGroup[dataset$Fare >= fares[1] & dataset$Fare < fares[2]] <- 'M'
    dataset$FareGroup[dataset$Fare >= fares[3]] <- 'H'
    # IMPORTANT: This will aggregate dataseting dataset based on FareGroup, Pclass and Sex columns
    if (view_process)
    {
        print (aggregate(Survived ~ FareGroup + Pclass + Sex, dataset, FUN=function(x) {sum(x)/length(x)}))
        # These indicte that females of 3rd class didn't have low chances of Survival
    }
    
    # Add a column and set to 1 where the passenger has reserved cabin(s)
    dataset$HasCabin <- 0
    dataset$HasCabin[dataset$Cabin != ""] <- 1
    # IMPORTANT: This will aggregate dataseting dataset based on HasCabin and Sex columns
    if (view_process)
    {
        print (aggregate(Survived ~ Cabin + Sex, dataset, FUN=function(x) {sum(x)/length(x)}))
        # These indicte does not show any special signifiance of presence of a Cabin
    }
    
    # THAT'S IT! NOW WE APPLY WHAT WE HAVE LEARNT
    dataset$PredSurvived <- 0
    dataset$PredSurvived[dataset$AgeGroup == "Child"] <- 1 # Let all females survive
    dataset$PredSurvived[dataset$Sex == "female"] <- 1 # Let all females survive
    dataset$PredSurvived[dataset$Sex == "female" & dataset$Pclass == 3] <- 0 # Females in 3rd class do not survive
    #    dataset$PredSurvived[dataset$Sex == 'male' & dataset$Pclass == 1 & dataset$FareGroup == 'H'] <- 1 # High paying, 1st class males survive too
    
    # Save the predicted Survived to file
    submit <- data.frame(PassengerId = dataset$PassengerId, Survived = dataset$PredSurvived)
    write.csv(submit, file=output_file, row.names=FALSE)
}

analyze_decisiontree <- function(training_data_file, test_data_file, output_file="mydecisiontreemodel_R.csv", mode="test")
{
    # Read the training data
    dataset <- read.csv(training_data_file)
    testset <- read.csv(test_data_file)
    
    if (mode == "train")
    {
        # Break the dataset into 2 parts, creating a test set of 10% random records and removing them from dataset
        testset <- dataset[sample(1:nrow(dataset), round(nrow(dataset)/10), replace="F"),]
        dataset <- subset(dataset, !(dataset$PassengerId %in% testset$PassengerId))
    }
    
    # Fill in missing values with average age
    bad <- is.na(dataset$Age)
    dataset$Age[bad] <- round(mean(dataset$Age[!bad]))
    bad <- is.na(testset$Age)
    testset$Age[bad] <- round(mean(testset$Age[!bad]))
    
    # Fill in missing values with average fare
    bad <- is.na(dataset$Fare)
    dataset$Fare[bad] <- round(mean(dataset$Fare[!bad]))
    bad <- is.na(testset$Fare)
    testset$Fare[bad] <- round(mean(testset$Fare[!bad]))
    
    # Add a column to check if a Passenger reserved a Cabin
    dataset$HasCabin <- 0
    dataset$HasCabin[dataset$Cabin != ""] <- 1
    testset$HasCabin <- 0
    testset$HasCabin[testset$Cabin != ""] <- 1
    
    # ROCKET SCIENCE! The method below uses Random Partitioning function
    fit <- rpart(Survived ~ Sex + Pclass + Age + SibSp + Parch + Fare + Embarked + HasCabin, 
                 data=dataset, method="class", control=rpart.control(minsplit=10, cp=0,  maxdepth=3))
    fancyRpartPlot(fit)
    
    # Save the predicted Survived to file
    testset$PredSurvived <- predict(fit, testset, type="class")
    submit <- data.frame(PassengerId = testset$PassengerId, Survived = testset$PredSurvived)
    write.csv(submit, file=output_file, row.names=FALSE)
    
    # Print the accuracy (true predictions / total passengers) (only for training data)
    if (mode == "train")
    {
        print (length(testset$Survived[testset$Survived == testset$PredSurvived])/nrow(testset))
    }
}

analyze_decisiontree <- function(training_data_file, test_data_file, output_file="myrandomforestmodel_R.csv", mode="test")
{
    if (mode == "test")
    {
        test_data_file <- "test.csv"
    }
    # Read the training data
    dataset <- read.csv(training_data_file)
    testset <- read.csv(test_data_file)
    
    # Break the dataset into 2 parts, creating a test set of 10% random records and removing them from dataset
    if (mode == "train")
    {
        testset <- dataset[sample(1:nrow(dataset), round(nrow(dataset)/5), replace="F"),]
        dataset <- subset(dataset, !(dataset$PassengerId %in% testset$PassengerId))
    }
    
    # First, we need to fill in missing values, not by mean value, but using Random partitioning method to predict them
    bad <- is.na(dataset$Age)
    age_fit <- rpart(Age ~ Sex + Pclass + SibSp + Parch + Fare + Embarked, data=dataset[!bad,], method="anova")
    dataset$Age[bad] <- predict(age_fit, dataset[bad,])
    bad <- is.na(testset$Age)
    age_fit <- rpart(Age ~ Sex + Pclass + SibSp + Parch + Fare + Embarked, data=testset[!bad,], method="anova")
    testset$Age[bad] <- predict(age_fit, testset[bad,])
    
    # Fill missing fares with average
    bad <- is.na(dataset$Fare)
    dataset$Fare[bad] <- round(mean(dataset$Fare[!bad]))
    bad <- is.na(testset$Fare)
    testset$Fare[bad] <- round(mean(testset$Fare[!bad]))
    
    # Fill missing ports with most frequent
    dataset$Embarked[dataset$Embarked == ""] <- 'S'
    dataset$Embarked <- factor(dataset$Embarked)
    testset$Embarked[testset$Embarked == ""] <- 'S'
    testset$Embarked <- factor(testset$Embarked)
    
    # Add a column to check if a Passenger reserved a Cabin
    dataset$HasCabin <- 0
    dataset$HasCabin[dataset$Cabin != ""] <- 1
    testset$HasCabin <- 0
    testset$HasCabin[testset$Cabin != ""] <- 1
    
    # ROCKET SCIENCE! The method below uses Random Forest function. Random Forests are decision trees that keep different attributes on different levels of hierarchy, then vote among the forest to decide which node survives. Source: http://trevorstephens.com/post/73770963794/titanic-getting-started-with-r-part-5-random
    rf_fit <- randomForest(as.factor(Survived) ~ Pclass + Sex + Age + SibSp + Parch + Fare + Embarked + HasCabin, data=dataset, 
                           importance=TRUE, ntree=2000, control=rpart.control(minsplit=10, cp=0,  maxdepth=3))
    varImpPlot(rf_fit)
    
    # Save the predicted Survived to file
    testset$PredSurvived <- predict(rf_fit, testset)
    submit <- data.frame(PassengerId=testset$PassengerId, Survived=testset$PredSurvived)
    write.csv(submit, file=output_file, row.names=FALSE)
    
    # Print the accuracy (true predictions / total passengers) (only for training data)
    if (mode == "train")
    {
        print (length(testset$Survived[testset$Survived == testset$PredSurvived])/nrow(testset))
    }
}