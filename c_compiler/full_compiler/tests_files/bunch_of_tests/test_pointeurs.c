#include <stdio.h>

int main() {
    int a = 10;
    int* p = &a;
    printf("Valeur de a: %d\n", a);
    printf("Valeur pointe par p: %d\n", *(p + 1 - 1));
    *(p + 1 - 1) = 20;
    int* q = p - 1;
    printf("Valeur de a: %d\n", a);
    *(q + 1) = 25;
    printf("Valeur de a: %d\n", a);
    int** pp = &p;
    *(*pp) = 30;
    printf("Valeur de a: %d\n", *(*pp));
    printf("Valeur de a: %d\n", *p);
    printf("Valeur de a: %d\n", a);
    return 0;
}
