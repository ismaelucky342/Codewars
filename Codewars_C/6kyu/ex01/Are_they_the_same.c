#include <stdbool.h>
#include <stddef.h>

// Helper function to find the index of an element in an array, -1 if not found
int find_index(int arr[], size_t n, int value) {
    for (size_t i = 0; i < n; i++) {
        if (arr[i] == value) {
            return i;
        }
    }
    return -1;
}

bool comp(const int a[], const int b[], size_t n) {
    if (a == NULL || b == NULL) {
        return false;
    }

    // Create a copy of array b so we can modify it
    int b_copy[n];
    for (size_t i = 0; i < n; i++) {
        b_copy[i] = b[i];
    }

    // Check if each element in a squared exists in b
    for (size_t i = 0; i < n; i++) {
        int squared = a[i] * a[i];
        int index = find_index(b_copy, n, squared);
        if (index == -1) {
            return false; // squared value not found in b_copy
        }
        b_copy[index] = -1; // Mark as used
    }

    return true;
}
