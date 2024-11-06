### **Different lists?**

Here are two lists. They each represent a sample of observations of some value taken from some larger population of values:

```r
g1 <- c(124, 118, 78, 123, 124, 124)
g2 <- c(127, 125, 125, 125, 172, 125)

```

Did these come from the same population? It's hard to say. We don't know what they are. Maybe the number of people enrolled in an introductory statistics class? Maybe systolic blood pressure measurements? Maybe my golf scores?

### **Some things to notice**

You'll notice the smallest value in g2 is larger than the biggest in g1, but the variance of each sample is pretty big, so again, it's hard to say. Let's focus on the mean values: the mean of g1 is about `117.17`, for g2 it's `136.5`, and the absolute difference is about `19.33`.

### **Don't do it this way**

We could compute a two-sided t-test on the sample means, but we'd be out on a limb with that one, since, again, we can't say anything about the distribution of the values in the population they come from. Lets do that (**DON'T DO THAT**): assuming equal variances (they're about equal), we get a p-value of `0.1265`. So they look a little different, but really not that different, and not different enough to satisfy the good folks at Guinness in 1908.

### **Do it this way**

Lets try this: if they are from the same population, i.e., *if the measurement is independent of the group assignment*, then we can assign measurement values to whichever group we'd like. It's like probability with counting. We can partition the 12 measurements above, 6 in group g1 and 6 in g2, in all the different ways possible, and then *count how many times the sample statistic (absolute difference between sample means) is equal or greater than the sample statistic (absolute difference between sample means) in observation we were given to begin with*. This is what is known as a [**permutation test**](https://en.wikipedia.org/wiki/Resampling_%28statistics%29#Permutation_tests). Do that. Make it exact.

# **Task:**

Write a function, `exact_p(g1, g2)` that takes two samples g1 and g2, and computes a p-value for the difference in sample means using a permutation test.

### **Some things to remember:**

1. Given all possible partitions of the data into equal size groups, `p` is the proportion of those partitions with an ABSOLUTE difference in sample means EQUAL or GREATER than the original partition.
2. As implied by item 1, `0 < p < 1`
3. As with the example, samples g1 and g2 will always have the same length, have non-overlapping ranges, and you can assume equal variances.
4. Your function will be tested with samples of length 2 to 9 (no empty lists, no lists of length 1)
5. Results are rounded to 4 decimal places when tested, so I suppose you have a chance with a Monte Carlo approach.

# **Examples**

```r
exact_p(c(124, 118, 78, 123, 124, 124), c(127, 125, 125, 125, 172, 125))
[1] 0.002164502
exact_p(c(12705, 12264, 12003, 12536), c(13524, 13478, 12845, 13351))
[1] 0.02857143

```

Note: rounding the result may result in some random tests expecting a value of 0. That doesn't mean it expects your p value to be 0, it just expects it to be less than 0.00005. The p value of an exact permutation test can never be 0. Understanding that will help you solve this kata!

If you want to try finding an exact p for two groups with overlapping ranges, try this one [**Exact p**](https://www.codewars.com/kata/59baf6676a9b6053950007b1)