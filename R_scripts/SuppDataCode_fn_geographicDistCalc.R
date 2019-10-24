############
#fn_geographicDistCalc
#Created on 7.19.2017

#Calculates the great circle distance between latitude,longitude pairs to give a pairwise distance matrix for geographical locations.
###########

fn_geographicDistCalc <- function(LatLongMatrix, outputDistMatrixFileName){
  
  #check/set whether you want to write the output to file
  wantToWrite <- !missing(outputDistMatrixFileName)
  
  #functions for cacluating great circle distance
  deg2rad <- function(deg) return(deg*pi/180)
  
  gcd.slc <- function(long1, lat1, long2, lat2) {
    R <- 6371 # Earth mean radius [km]
    d <- acos(sin(lat1)*sin(lat2) + cos(lat1)*cos(lat2) * cos(long2-long1)) * R
    return(d) # Distance in km
  }
  
  #calculate pairwise distances -> output is symmetric distance matrix
  NUMSAMPLES = nrow(LatLongMatrix)
  GeoDistanceMatrix=matrix(0,NUMSAMPLES,NUMSAMPLES) 
  
  for(i in 1:NUMSAMPLES){
    for(j in 1:NUMSAMPLES){
      lat1=LatLongMatrix[i,1]   #make sure that column 1 is lat and column 2 is long in the matrix passed to the function
      long1=LatLongMatrix[i,2]
      lat2=LatLongMatrix[j,1]
      long2=LatLongMatrix[j,2]
      GeoDistanceMatrix[i,j]=gcd.slc(deg2rad(long1), deg2rad(lat1), deg2rad(long2), deg2rad(lat2))
    }
  }
  
  rownames(GeoDistanceMatrix) <- row.names(LatLongMatrix)
  colnames(GeoDistanceMatrix) <- row.names(LatLongMatrix)
  
  #write symmetric distance matrix to text file
  if (wantToWrite){
    write.table(GeoDistanceMatrix, paste(outputDistMatrixFileName,".txt"), sep="\t") 
  }
  
  return(GeoDistanceMatrix)
  
}










