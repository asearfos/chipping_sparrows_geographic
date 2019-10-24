############
#ChippingSparrowDistAnalysis
#Created on 7.19.2017

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

#file names of text files with your geographic information and genetic information 
#geographic file should be tab deliminated with column headers, each row is information for a single sample
#genetic file should be a fasta file of aligned sequences
geoFileName = "Mila_ControlRegionSeq/Mila_HaplotypeToLocation_correctedCA_allSamples.txt"
geneFileName = "Mila_ControlRegionSeq/Mila_ControlRegionSeq_aligned_allSamples.fasta"

###LOAD FILES###

#read in geographical data
dataTable=read.table(geoFileName, header=T, sep="\t")

#read in genetic data, convert to matrix
geneData = read.fasta(geneFileName) #this reads in as a list
geneMatrix = do.call(rbind,geneData) #convert to matrix

#clean data (rm those with limited data) --> with updated FASTA with all samples, this is no longer necessary
na_coord  = !rowSums(is.na(dataTable[,c("Latitude","Longitude")]))
dataTable_new = dataTable[na_coord,]
geneMatrix_new = geneMatrix[na_coord,]

#sort data by latitude, largest (North) to smallest (South)
dataTable_newLatSort = dataTable_new[rev(order(dataTable_new[,c("Latitude")])),] 
geneMatrix_newLatSort = geneMatrix_new[rev(order(dataTable_new[,c("Latitude")])),]

#data indices by geographical location
US = which(dataTable_newLatSort$Country == "United States")
CA = which(dataTable_newLatSort$Country == "Canada") #Canada only has few data points, so too small for analysis
MX = which(dataTable_newLatSort$Country == "Mexico")
GT = which(dataTable_newLatSort$Country == "Guatemala")


###CALCULATE DISTANCE MATRICES###

#calculate geographical distance matrices
source("fn_geographicDistCalc.R")

geoDist_latSort = fn_geographicDistCalc(as.matrix(dataTable_newLatSort[,c("Latitude","Longitude")]))

geoDist_US_CA = fn_geographicDistCalc(as.matrix(dataTable_newLatSort[c(US,CA),c("Latitude","Longitude")]))
geoDist_MX_GT = fn_geographicDistCalc(as.matrix(dataTable_newLatSort[c(MX,GT),c("Latitude","Longitude")]))
geoDist_US_CA_MX = fn_geographicDistCalc(as.matrix(dataTable_newLatSort[c(US,CA,MX),c("Latitude","Longitude")]))

geoDist_US = fn_geographicDistCalc(as.matrix(dataTable_newLatSort[US,c("Latitude","Longitude")]))
geoDist_MX = fn_geographicDistCalc(as.matrix(dataTable_newLatSort[MX,c("Latitude","Longitude")]))
geoDist_GT = fn_geographicDistCalc(as.matrix(dataTable_newLatSort[GT,c("Latitude","Longitude")]))

#calculate genetic distance matrices
source("fn_geneticDistCalc.R") #note this function returns two distance matrices, calcuated using different packages/methods

geneDistMatrices_latSort = fn_geneticDistCalc(geneMatrix_newLatSort)
geneDist_latSort = geneDistMatrices_latSort[[1]]
geneDist_k80_latSort = geneDistMatrices_latSort[[2]]

geneDistMatrices_US_CA = fn_geneticDistCalc(geneMatrix_newLatSort[c(US,CA),])
geneDistMatrices_MX_GT = fn_geneticDistCalc(geneMatrix_newLatSort[c(MX,GT),])
geneDistMatrices_US_CA_MX = fn_geneticDistCalc(geneMatrix_newLatSort[c(US,CA,MX),])

geneDistMatrices_US = fn_geneticDistCalc(geneMatrix_newLatSort[US,])
geneDistMatrices_MX = fn_geneticDistCalc(geneMatrix_newLatSort[MX,])
geneDistMatrices_GT = fn_geneticDistCalc(geneMatrix_newLatSort[GT,])


###RUN MATNEL TESTS###

#run mantel test on the two distance matrices - one of geographical dist. and one genetic dist.
#do this for all samples and then also subset categories based on country the samples are from
# overallMantel = mantel(geoDist_latSort, geneDist_latSort, method ="pearson", permutations=1000000)
# mantel_US_CA = mantel(geoDist_US_CA, geneDistMatrices_US_CA[[1]], method ="pearson", permutations=1000000)
# mantel_MX_GT = mantel(geoDist_MX_GT, geneDistMatrices_MX_GT[[1]], method ="pearson", permutations=1000000)
# mantel_US_CA_MX = mantel(geoDist_US_CA_MX, geneDistMatrices_US_CA_MX[[1]], method ="pearson", permutations=1000000)
# mantel_US = mantel(geoDist_US, geneDistMatrices_US[[1]], method ="pearson", permutations=1000000)
# mantel_MX = mantel(geoDist_MX, geneDistMatrices_MX[[1]], method ="pearson", permutations=1000000)
# mantel_GT = mantel(geoDist_GT, geneDistMatrices_GT[[1]], method ="pearson", permutations=1000000)

#same thing for second type of genetic dist calculation
overallMantel_k80 = mantel(geoDist_latSort, geneDist_k80_latSort, method ="pearson", permutations=1000000)
mantel_US_CA_k80 = mantel(geoDist_US_CA, geneDistMatrices_US_CA[[2]], method ="pearson", permutations=1000000)
mantel_MX_GT_k80 = mantel(geoDist_MX_GT, geneDistMatrices_MX_GT[[2]], method ="pearson", permutations=1000000)
mantel_US_CA_MX_k80 = mantel(geoDist_US_CA_MX, geneDistMatrices_US_CA_MX[[2]], method ="pearson", permutations=1000000)
mantel_US_k80 = mantel(geoDist_US, geneDistMatrices_US[[2]], method ="pearson", permutations=1000000)
mantel_MX_k80 = mantel(geoDist_MX, geneDistMatrices_MX[[2]], method ="pearson", permutations=1000000)
mantel_GT_k80 = mantel(geoDist_GT, geneDistMatrices_GT[[2]], method ="pearson", permutations=1000000)





