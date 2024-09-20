#include <stdio.h>
#include <stdlib.h>

int maxSum(int a, int b) {
    return a > b ? a : b;
}

// Helper function to generate combinations and calculate the best sum
void combine(int *ls, int szls, int k, int t, int start, int *combination, int combSize, int *bestSum) {
    if (combSize == k) {
        int sum = 0;
        for (int i = 0; i < k; i++) {
            sum += combination[i];
        }
        if (sum <= t) {
            *bestSum = maxSum(*bestSum, sum);
        }
        return;
    }
    for (int i = start; i < szls; i++) {
        combination[combSize] = ls[i];
        combine(ls, szls, k, t, i + 1, combination, combSize + 1, bestSum);
    }
}

int chooseBestSum(int t, int k, int ls[], int szls) {
    int bestSum = -1;
    int *combination = (int*)malloc(k * sizeof(int));
    combine(ls, szls, k, t, 0, combination, 0, &bestSum);
    free(combination);
    return bestSum;
}