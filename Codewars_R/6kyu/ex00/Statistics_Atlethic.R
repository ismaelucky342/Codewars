stat <- function(results) {
    if (results == "") {
        return("")
    }
    
    # Split the input into individual results
    time_strings <- unlist(strsplit(results, ",\\s*|,"))
    
    # Convert time strings into total seconds
    total_seconds <- sapply(time_strings, function(ts) {
        parts <- as.integer(unlist(strsplit(ts, "\\|")))
        return(parts[1] * 3600 + parts[2] * 60 + parts[3])
    })
    
    # Calculate Range
    range_value <- max(total_seconds) - min(total_seconds)
    
    # Calculate Average
    average_value <- mean(total_seconds)
    
    # Calculate Median
    sorted_seconds <- sort(total_seconds)
    n <- length(sorted_seconds)
    median_value <- if (n %% 2 == 1) {
        sorted_seconds[(n + 1) / 2]
    } else {
        (sorted_seconds[n / 2] + sorted_seconds[n / 2 + 1]) / 2
    }
    
    # Helper function to convert seconds back to hh|mm|ss
    format_time <- function(total_sec) {
        # Ensure total_sec is numeric and then calculate h, m, s
        total_sec <- as.numeric(total_sec)
        h <- floor(total_sec / 3600)
        m <- floor((total_sec %% 3600) / 60)
        s <- total_sec %% 60
        # Return formatted string
        return(sprintf("%02d|%02d|%02d", as.integer(h), as.integer(m), as.integer(s)))
    }
    
    # Format results
    range_str <- format_time(range_value)
    average_str <- format_time(average_value)
    median_str <- format_time(median_value)
    
    # Return the final string
    return(sprintf("Range: %s Average: %s Median: %s", range_str, average_str, median_str))
}

# Example Usage
result <- stat("01|15|59, 1|47|6, 01|17|20, 1|32|34, 2|3|17")
print(result)