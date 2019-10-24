############
#fn_geneticDistCalc
#Created on 7.13.2017

#Creates a pairwise distance matrix between the DNA sequences. Does this using two different methods (dist.gene -> #differences/#comparisons, dis.dna -> biologically informed) in order to compare.
###########

fn_geneticDistCalc <- function(seqMatrix, outputDistMatrixFileName){
  
  #read in all libraries needed
  library(seqinr)
  library(ape)
  
  #is an output path given to write results to file?
  wantToWrite <- !missing(outputDistMatrixFileName)
  
  #calculate distance matrix using two different methods, output is of class dist
  seq_distGene = dist.gene(seqMatrix, "percentage", pairwise.deletion = TRUE, variance = TRUE) #simply number of difference/number of comparisons
  seq_distDNA = dist.dna(as.DNAbin(seqMatrix), model = "K80", variance = TRUE, pairwise.deletion = TRUE) #Kimura's 2-parameter distance
  
  #write symmetric distance matrices to txt files
  if (wantToWrite){
    write.table(as.matrix(seq_distGene), paste(outputDistMatrixFileName,".txt"), sep="\t")
    write.table(as.matrix(seq_distDNA), paste(outputDistMatrixFileName,"_k80.txt"), sep="\t")
  } 
  
  output <- list(seqDist = seq_distGene, seqDist_k80 = seq_distDNA)
  return(output)
  
}