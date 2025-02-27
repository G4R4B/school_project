#include <stdio.h>

int main() {
    int a = 10;
    int b = 20;
    int c = ((a + b) * 2) - 5;
    int d = c + 5;
    printf("Le résultat de l'expression est %d\n", d + 10);
    a = 5;
    int result = (a++);
    int result2 = (++a);
    printf("Résultat: %d %d\n", result, result2);
    result = 1 + 2 * 3 + 4 * a + a;
    result2 = (1 + (2 * 3)) + ((4 * a) + a);
    printf("Résultat 1: %d, Résultat 2: %d\n", result, result2);  // Attendu: Les deux devraient donner le même résultat: 1 + 6 + 20 + 6 = 3
    return 0;
}