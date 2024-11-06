exact_p <- function(g1, g2) {
  # Combine the two groups
  combined <- c(g1, g2)
  n <- length(g1)  # Number of observations in each group
  
  # Calculate the observed difference in means
  observed_diff <- abs(mean(g1) - mean(g2))
  
  # Initialize a counter for the number of permutations with greater or equal difference
  count <- 0
  total_permutations <- 0
  
  # Generate all combinations of indices for the first group
  indices <- combn(length(combined), n)
  
  # Loop through each combination
  for (i in 1:ncol(indices)) {
    group1_indices <- indices[, i]
    group1 <- combined[group1_indices]
    group2 <- combined[-group1_indices]
    
    # Calculate the absolute difference of means for this permutation
    permuted_diff <- abs(mean(group1) - mean(group2))
    
    # Check if the permuted difference is greater than or equal to the observed difference
    if (permuted_diff >= observed_diff) {
      count <- count + 1
    }
    total_permutations <- total_permutations + 1
  }
  
  # Calculate the p-value
  p_value <- count / total_permutations
  
  return(round(p_value, 8))  # Return the p-value rounded to 8 decimal places
}