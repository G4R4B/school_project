#include <stdio.h>

// Fonction pour échanger deux éléments
void swap(int *a, int *b) {
    printf("Swapping %p and %p\n", a, b);
    int temp = *a;
    *a = *b;
    *b = temp;
}

// Tri par boucles imbriquées
void loopedBubbleSort(int arr[], int n) {
    // Exécuter plusieurs passes sur le tableau
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            if (arr[j] > arr[i]) {
                printf("Swapping %d and %d\n", arr[j], arr[i]);
                printf("Addresses: %p and %p\n", arr + j, arr + i);
                swap(&arr[j], &arr[i]);
                printf("After swap: ");
                printArray(arr, n);
            }
        }
    }
}

// Fonction pour afficher le tableau
void printArray(int arr[], int n) {
    for (int i = 0; i < n; i++) {
        printf("%d ", arr[i]);
    }
    printf("\n");
}

// Programme principal
int main() {
    int arr[5] = {5, 3, 8, 6, 2};
    int n = sizeof(arr) / sizeof(arr[0]);

    printf("Tableau original: ");
    printArray(arr, n);

    loopedBubbleSort(arr, n);

    printf("Tableau trié: ");
    printArray(arr, n);

    return 0;
}
