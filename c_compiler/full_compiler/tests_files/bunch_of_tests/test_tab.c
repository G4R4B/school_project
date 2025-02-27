#include <stdio.h>

int t[1000];


int main() {
    int i;
    for (i = 0; i < 1000; i++) {
        t[i] = i;
    }
    for (i = 0; i < 1000; i++) {
        printf("%d ", t[i]);
    }

    return 0;
}