#include <stdio.h>

int f(int arr[]){
    printf("Valeur de arr[0]: %d\n", arr[0]);
    return 0;
}

int main(){
    int arr[10];
    arr[0] = 1;
    f(arr);
    return 0;
}