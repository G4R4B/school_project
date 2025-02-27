#include <stdio.h>

int main() {
    int arr[5] = {10, 20, 30, 40, 50};
    int *p = arr;
    int result = *(p + 2) + *(p + 4) - *(p + 1);
    printf("Result of complex expression *(p+2) + *(p+4) - *(p+1): %d\n", result); // Expect 30 + 50 - 20 = 60

    // Reset pointer to middle of the array
    p = arr + 2;
    printf("Reset pointer to middle, value at p: %d\n", *p); // Expect 30

    return 0;
}