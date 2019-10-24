############
#ChippingSparrowDistAnalysisBarcodes
#Created on 5.10.2018 (from ChippingSparrowDistAnalysis)

#Loads in geographical and genetic data of interest. Removes any data that does not have enough geographical information.
#Calls functions to calculate distance matrices for both geographical and genetic data.
#Runs mantel test on a set of geographical and genetic data. 
###########

rm(list = ls())

#load libraries
library(vegan)
library(seqinr)
library(ggplot2)
library(ape)
library(dplyr)
library(foreach)
library(doParallel)

start_time <- Sys.time()

#set working directory
setwd("")

songFileName = "AnimalBehaviour_SupplementalDataTable2_addedMid.csv"

###LOAD FILES###

#read in geographical data
fullDataTable = read.table(songFileName, header=T, sep=",")

songData = fullDataTable[fullDataTable$ComparedStatus != 'duplicate', ]
songData_LatSort = songData[rev(order(songData[,c("Latitude")])),] 

#calculate geographical distance matrices
source("fn_geographicDistCalc.R")

songDist_latSort = fn_geographicDistCalc(as.matrix(songData_LatSort[,c("Latitude","Longitude")]))

mantel_results <- data.frame(matrix(ncol = 2, nrow = 16))
variables <- c(colnames(songData_LatSort[11:26]))
rownames(mantel_results) <- variables
colnames(mantel_results) <- c("stat", "p")

for (i in 1:16){
  varDist_LatSort = as.matrix(dist(songData_LatSort[10+i], diag=TRUE, upper=TRUE))
  col_tmp <- colnames(songData_LatSort)[10+i]
  print(col_tmp)
  mantel_tmp <- mantel(songDist_latSort, varDist_LatSort, method ="pearson", permutations=10000)
  mantel_results[i, "stat"] <- mantel_tmp$statistic
  mantel_results[i, "p"] <- mantel_tmp$signif
}


write.table(mantel_results, paste("outputMantelResultsForSong",".txt"), sep="\t") 

#downsampling

songData_LatSort_Round=songData_LatSort
songData_LatSort_Round$Latitude=round(songData_LatSort_Round$Latitude,2)
songData_LatSort_Round$Longitude=round(songData_LatSort_Round$Longitude,2)
songData_LatSort_Round=cbind(c(1:820),songData_LatSort_Round)
names(songData_LatSort_Round)[1]="Index"


seed_list = read.table('RandomSeeds.csv', header=F, sep=",")

#setup parallel backend to use many processors
cores=detectCores()
cl <- makeCluster(cores[1]-1) #not to overload your computer
registerDoParallel(cl)

mantel_p_matrix=c(0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)
for (j in 1:1000){
  start_time2 <- Sys.time()
  
  set.seed(seed_list[j,])
  songData_LatSort_SUBSET <- songData_LatSort_Round %>% group_by(songData_LatSort_Round$Latitude,songData_LatSort_Round$Longitude) %>% sample_n(1)
  songdistSUBSET=songDist_latSort[songData_LatSort_SUBSET$Index,songData_LatSort_SUBSET$Index]
  print(j)
  mantel_p_row <- foreach(i=1:16, .combine=cbind, .packages=c("dplyr", "vegan")) %dopar% {
    varDist_LatSortSUBSET = as.matrix(dist(songData_LatSort_SUBSET[11+i], diag=TRUE, upper=TRUE))
    mantel_tmp <- mantel(songdistSUBSET, varDist_LatSortSUBSET, method ="pearson", permutations=10000)
    mantel_tmp$signif
  }
  mantel_p_matrix=rbind(mantel_p_matrix,mantel_p_row)
  
  end_time2 <- Sys.time()
  print(end_time2 - start_time2)
}

mantel_p_matrix=mantel_p_matrix[-1,]
colnames(mantel_p_matrix) <- variables
stopCluster(cl)
