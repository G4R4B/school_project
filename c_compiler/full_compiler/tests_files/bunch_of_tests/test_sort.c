#include <stdio.h>
#include <stdlib.h>

int main() {
    // Initialize the array
    int arr[1000];
    int n = 1000;
    for (int i = 0; i < n; i++) {
        arr[i] = n - i;
    }

    // Perform Bubble Sort
    for (int i = 0; i < n - 1; i++) {
        // Last i elements are already sorted
        for (int j = 0; j < n - i - 1; j++) {
            // Compare adjacent elements
            if (arr[j] > arr[j + 1]) {
                // Swap if they are in the wrong order
                int temp = arr[j];
                arr[j] = arr[j + 1];
                arr[j + 1] = temp;
            }
        }
    }

    // verify the result
    for (int i = 0; i < n - 1; i++) {
        printf("%d ", arr[i]);
        printf("%d ", arr[i + 1]);
        printf("\n");
        if (arr[i] > arr[i + 1]) {
            printf("Sort failed\n");
            return 1;
        }
    }
    printf("\n");

    return 0; // Exit successfully
}
