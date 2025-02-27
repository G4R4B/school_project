#include <stdio.h>

int main() {
    for (int i = 0; i < 100; i++) {
        if (i == 50) {
            printf("Boucle interrompue à i = %d\n", i);
            break;
        }
        printf("i = %d\n", i);
    }
    return 0;
}
