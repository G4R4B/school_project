#include <stdio.h>

int func1(int tab[]){
    return tab[1];
}

int main() {
    int arr[5] = {1, 2, 3, 4, 5};
    printf("arr[%d] = %d\n", 0, arr[1]);
    arr[2] = arr[1] + arr[3];
    printf("arr[%d] = %d\n", 0, func1(arr));
    printf("arr[%d] = %d\n", 2, func1(arr));
    return 0;
}
