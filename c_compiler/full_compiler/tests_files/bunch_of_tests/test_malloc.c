#include <stdio.h>
#include <stdlib.h>

int fat(int* p){
    printf("%d\n", p[500]);
}

int main() {
    // Allocate memory for an array of 1000 integers
    int* t = malloc(1000*8);
    printf("%p\n", t);
    for (int i = 0; i < 1000; i++) {
        t[i] = i; // Assign each element its index value
    }
    printf("%p\n", t);
    fat(t);
    printf("%p\n", t);
    // // Read and print the values in the array
    // for (int i = 0; i < 1000; i++) {
    //     printf("t[%d] = %d\n", i, t[i]);
    // }

    // Free the allocated memory
    free(t);
    return 0; // Exit successfully
}
