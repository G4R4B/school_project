#include <stdio.h>

void recursive_function_tests(int depth) {
    if (depth == 0) {
        return;
    }

    int a = depth;
    int b = depth * 2;

    // Testing recursive function with if-else, both branches with blocks
    if (a % 2 == 0) {
        {
            printf("Depth %d: Even case reached, depth = %d\n", depth, a);
            recursive_function_tests(depth - 1);
        }
    } else {
        {
            printf("Depth %d: Odd case reached, depth = %d\n", depth, a);
            recursive_function_tests(depth - 1);
        }
    }
}

void while_loop_with_break_continue() {
    int i = 0;

    printf("\nTesting while loop with break and continue...\n");
    while (i < 10) {
        if (i == 5) {
            printf("Reached %d, using break to exit loop\n", i);
            break;
        }
        if (i % 2 == 0) {
            printf("%d is even, using continue to skip to next iteration\n", i);
            i++;
            continue;
        }
        printf("Current value: %d\n", i);
        i++;
    }
}
int somme(int n) {
    if (n <= 0) { // Cas de base
        return 0;
    } else { // Cas récursif
        return n + somme(n - 1);
    }
}


int main() {
    printf("Testing recursive functions with if-else blocks...\n");
    recursive_function_tests(6);

    while_loop_with_break_continue();
    int n = 10000;
    printf("Somme de %d: %d\n",n, somme(n));
    printf("Vrai somme de %d : %d\n", n, n*(n+1)/2);

    return 0;
}
