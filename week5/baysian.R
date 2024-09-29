install.packages("bnlearn", repos = "http://cran.us.r-project.org")
install.packages("e1071", repos = "http://cran.us.r-project.org")
install.packages("caret", repos = "http://cran.us.r-project.org")

library(bnlearn)
library(caret)
library(e1071)

grades <- c("AA", "AB", "BB", "BC", "CC", "CD", "DD", "F")
course.grades <- read.table("2020_bn_nb_data.txt", head=TRUE)
course.grades[] <- lapply(course.grades, function(x) if (is.character(x)) as.factor(x) else x)

str(course.grades)

course.grades.net <- hc(course.grades, score = "k2")
course.grades.bn.fit <- bn.fit(course.grades.net, course.grades)
prob <- 0.0
ans = ""
for(value in grades) {
  p <- cpquery(course.grades.bn.fit, event = (PH100 == value), evidence = (EC100 == "DD" & IT101 == "CC" & MA101 == "CD"))
  if(p > prob) {
    ans <- value
    prob <- p
  }
}
print(paste("Most probable grade:", ans))

set.seed(100)
tIndex <- createDataPartition(course.grades$QP, p=0.7)$Resample1
train <- course.grades[tIndex, ]
test <- course.grades[-tIndex, ]

nbc <- naiveBayes(QP ~ EC100 + EC160 + IT101 + IT161 + MA101 + PH100 + PH160 + HS101, data = train)

printALL = function(model) {
  trainPred = predict(model, newdata = train, type = "class")
  trainTable = table(train$QP, trainPred)
  testPred = predict(nbc, newdata = test, type = "class")
  testTable = table(test$QP, testPred)
  
  trainAcc = sum(diag(trainTable)) / sum(trainTable)
  testAcc = sum(diag(testTable)) / sum(testTable)
  
  message("Accuracy")
  print(round(cbind("Training Accuracy" = trainAcc, "Test Accuracy" = testAcc), 4))
}

printALL(nbc)

trainda <- bn.fit(hc(train, score = "k2"), train)
predicted <- predict(trainda, node = "QP", data = test)
tabletrain <- table(test$QP, predicted)
trainAcc = (tabletrain[1,1] + tabletrain[2,2]) / sum(tabletrain)
message("Accuracy for Bayesian Network")
print(round(cbind("Training Accuracy" = trainAcc), 4))