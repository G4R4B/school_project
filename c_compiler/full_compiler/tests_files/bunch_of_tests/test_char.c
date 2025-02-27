#include <stdio.h>

int main() {
    // Déclaration de 16 tableaux de caractères
    char str1[50] = "Bonjour";
    char concat[200]; // Tableau pour stocker la chaîne concaténée
    int index = 0;

    // Concaténer les chaînes dans `concat`
    for (int i = 0; i < 50 && str1[i] != 0; i++) {
        concat[index] = str1[i];
        index++;
    }
    concat[index] = 0; // Ajout du caractère de fin de chaîne

    // Affichage de la chaîne concaténée
    printf("Chaîne concatenee : %s\n", concat);

    return 0;
}