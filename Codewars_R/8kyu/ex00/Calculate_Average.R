find_average <- function(vec) {
  if (length(vec) == 0) {
    return(0)
  }
  
  average <- sum(vec) / length(vec)
  return(average)
}
