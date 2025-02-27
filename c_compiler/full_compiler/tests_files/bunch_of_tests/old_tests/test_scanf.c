#include <stdio.h>

int main() {
    // Déclaration et manipulation de 15 blocs avec scanf et printf
    char c;
    int i;
    int array1[10];
    int array2[20];
    char str[50];

    // 1. Bloc de caractère
    printf("Entrez un caractère : ");
    scanf(" %c", &c);
    printf("Vous avez entré le caractère : %c\n", c);

    // 3. Bloc d'entier
    printf("Entrez un nombre entier (int) : ");
    scanf("%d", &i);
    printf("Vous avez entré l'entier : %d\n", i);

    // 7. Bloc de tableau d'entiers (10 éléments)
    printf("Entrez 10 entiers pour le tableau : ");
    for (int j = 0; j < 10; j++) {
        scanf("%d", &array1[j]);
    }
    printf("Vous avez entré le tableau de 10 entiers : ");
    for (int j = 0; j < 10; j++) {
        printf("%d ", array1[j]);
    }
    printf("\n");

    // 8. Bloc de tableau d'entiers (20 éléments)
    printf("Entrez 20 entiers pour le tableau : ");
    for (int j = 0; j < 20; j++) {
        scanf("%d", &array2[j]);
    }
    printf("Vous avez entré le tableau de 20 entiers : ");
    for (int j = 0; j < 20; j++) {
        printf("%d ", array2[j]);
    }
    printf("\n");

    // 9. Bloc de chaîne de caractères
    printf("Entrez une chaîne de caractères : ");
    scanf("%49s", str);
    printf("Vous avez entré la chaîne : %s\n", str);

    // 10. Bloc de caractère supplémentaire
    printf("Entrez un autre caractère : ");
    scanf(" %c", &c);
    printf("Vous avez entré le caractère : %c\n", c);

    // 12. Bloc d'entier supplémentaire
    printf("Entrez un autre nombre entier (int) : ");
    scanf("%d", &i);
    printf("Vous avez entré l'entier : %d\n", i);

    return 0;
}
