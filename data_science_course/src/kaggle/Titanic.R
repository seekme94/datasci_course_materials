library(rattle)
library(rpart.plot)
library(RColorBrewer)
library(rpart)
library(randomForest)

readData <- function(file.name, column.types, missing.types)
{
    read.csv(file.name, colClasses=column.types, na.strings=missing.types)
}

getTitle <- function(data) {
    title.dot.start <- regexpr("\\,[A-Z ]{1,20}\\.", data$Name, TRUE)
    title.comma.end <- title.dot.start 
    + attr(title.dot.start, "match.length")-1
    data$Title <- substr(data$Name, title.dot.start+2, title.comma.end-1)
    return (data$Title)
}

train.data.file <- "train.csv"
test.data.file <- "test.csv"
missing.types <- c("NA", "")
train.column.types <- c('integer',   # PassengerId
                        'factor',    # Survived 
                        'factor',    # Pclass
                        'character', # Name
                        'factor',    # Sex
                        'numeric',   # Age
                        'integer',   # SibSp
                        'integer',   # Parch
                        'character', # Ticket
                        'numeric',   # Fare
                        'character', # Cabin
                        'factor'     # Embarked
)
test.column.types <- train.column.types[-2] # no Survived column in test.csv

train.raw <- readData(train.data.file, train.column.types, missing.types)
df.train <- train.raw
test.raw <- readData(test.data.file, test.column.types, missing.types)
df.infer <- test.raw

# Visualize data
barplot(table(df.train$Survived), names.arg = c("Perished", "Survived"), main="Survived (passenger fate)", col="black")
barplot(table(df.train$Pclass), names.arg = c("first", "second", "third"), main="Pclass (passenger traveling class)", col="firebrick")
barplot(table(df.train$Sex), main="Sex (gender)", col="darkviolet")
hist(df.train$Age, main="Age", xlab = NULL, col="brown")
barplot(table(df.train$SibSp), main="SibSp (siblings + spouse aboard)", col="darkblue")
barplot(table(df.train$Parch), main="Parch (parents + kids aboard)", col="gray50")
hist(df.train$Fare, main="Fare (fee paid for ticket[s])", xlab = NULL, col="darkgreen")
barplot(table(df.train$Embarked), names.arg = c("Cherbourg", "Queenstown", "Southampton"), main="Embarked (port of embarkation)", col="sienna")

mosaicplot(df.train$Pclass ~ df.train$Survived, main="Passenger Fate by Traveling Class", shade=FALSE, color=TRUE, xlab="Pclass", ylab="Survived")
mosaicplot(df.train$Sex ~ df.train$Survived, main="Passenger Fate by Sex", shade=FALSE, color=TRUE, xlab="Sex", ylab="Survived")
mosaicplot(df.train$Embarked ~ df.train$Survived, main="Passenger Fate by Port Embarked", shade=FALSE, color=TRUE, xlab="Embarked", ylab="Survived")
mosaicplot(df.train$SibSp ~ df.train$Survived, main="Passenger Fate by Port Embarked", shade=FALSE, color=TRUE, xlab="Embarked", ylab="Survived")

df.train$Title <- getTitle(df.train)
unique(df.train$Title)

