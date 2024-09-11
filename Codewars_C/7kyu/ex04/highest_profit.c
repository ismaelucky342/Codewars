#include <limits.h>

void min_max(const int arr[], int count, int *min, int *max) {
    if (count == 0) {
        return;
    }
    
    *min = *max = arr[0];
    
    for (int i = 1; i < count; i++) {
        if (arr[i] < *min) {
            *min = arr[i]; // Update min if a smaller element is found
        }
        if (arr[i] > *max) {
            *max = arr[i]; // Update max if a larger element is found
        }
    }
}