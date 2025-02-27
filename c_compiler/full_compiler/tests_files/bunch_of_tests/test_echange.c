#include <stdio.h>

int valuea = 1;
int valueb = 2;

int f(int* a, int* b){
    int c = *a;
    *a = *b;
    *b = c;
    return 0;
}

int g(int* a){
    *a = 3;
    return 0;
}


int main(){
    int* a = &valuea;
    int* b = &valueb;
    *a = 1;
    *b = 2;
    printf("a = %d\n", *a);
    printf("b = %d\n", *b);
    f(a, b);
    printf("a = %d\n", *a);
    printf("b = %d\n", *b);
    g(a);
    printf("a = %d\n", *a);
    printf("b = %d\n", *b);
    return 0;
}