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

#set working directory
setwd("")

#file names
#geographic file should be tab deliminated with column headers, each row is information for a single sample
#genetic file should be a fasta file of aligned sequences
geoFileName = "ChippingSparrow_Barcodes_2017/ChippingSparrow_BarcodesToLocations.txt"
geneFileName = "ChippingSparrow_Barcodes_2017/ChippingSparrow_Barcodes_2017_aligned.fasta"

###LOAD FILES###

#read in geographical data
dataTable=read.table(geoFileName, header=T, sep="\t")

#read in genetic data, convert to matrix
geneData = read.fasta(geneFileName) #this reads in as a list
geneMatrix = do.call(rbind,geneData) #convert to matrix

#clean data (rm those with limited data)
na_coord  = !rowSums(is.na(dataTable[,c("Latitude","Longitude")]))
dataTable_new = dataTable[na_coord,]
geneMatrix_new = geneMatrix[na_coord,]

#sort data by latitude, largest (North) to smallest (South)
dataTable_newLatSort = dataTable_new[rev(order(dataTable_new[,c("Latitude")])),] 
geneMatrix_newLatSort = geneMatrix_new[rev(order(dataTable_new[,c("Latitude")])),]


###CALCULATE DISTANCE MATRICES###

#calculate geographical distance matrices
source("fn_geographicDistCalc.R")

geoDist_latSort = fn_geographicDistCalc(as.matrix(dataTable_newLatSort[,c("Latitude","Longitude")]))

#calculate genetic distance matrices
source("fn_geneticDistCalc.R") #note this function returns two distance matrices, calcuated using different packages/methods

geneDistMatrices_latSort = fn_geneticDistCalc(geneMatrix_newLatSort)
geneDist_latSort = geneDistMatrices_latSort[[1]]
geneDist_k80_latSort = geneDistMatrices_latSort[[2]]


###RUN MATNEL TESTS###

#run mantel test on the two distance matrices - one of geographical dist. and one genetic dist.
#overallMantel = mantel(geoDist_latSort, geneDist_latSort, method ="pearson", permutations=1000000)

#same thing for second type of genetic dist calculation
overallMantel_k80 = mantel(geoDist_latSort, geneDist_k80_latSort, method ="pearson", permutations=1000000)





