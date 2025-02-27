#include <stdio.h>

int main() {
    // Example using break
    printf("Using break:\n");
    int i = 0;
    while (1) {
        if (i == 5) {
            printf("Breaking the loop at i = %d\n", i);
            break; // Exit the loop when i is 5
        }
        printf("i = %d\n", i);
        i++;
    }

    printf("\nUsing continue:\n");
    // Example using continue
    i = 0;
    while (i < 10) {
        i++;
        if (i % 2 == 0) {
            printf("Skipping even number: %d\n", i);
            continue; // Skip the rest of the loop body for even numbers
        }
        printf("i = %d\n", i);
    }

    return 0; // Exit successfully
}
