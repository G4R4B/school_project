#include <stdio.h>
#include <stdbool.h>

// Variables globales pour observer les effets de bord
int f_calls = 0;
int g_calls = 0;

// Fonction f avec effet de bord (incrémente f_calls et retourne true ou false)
int f() {
    f_calls++;
    printf("f() appelé\n");
    return f_calls % 2 == 0;  // true une fois sur deux
}

// Fonction g avec effet de bord (incrémente g_calls et retourne true ou false)
int g() {
    g_calls++;
    printf("g() appelé\n");
    return g_calls % 3 != 0;  // false une fois sur trois
}

int main() {
    // Réinitialiser les compteurs d'appels
    f_calls = 0;
    g_calls = 0;

    // Combinaison 1 : f() && g()
    printf("Test 1: f() && g()\n");
    if (f() && g()) {
        printf("Condition f() && g() est vraie\n");
    } else {
        printf("Condition f() && g() est fausse\n");
    }
    printf("f_calls: %d, g_calls: %d\n\n", f_calls, g_calls);

    // Combinaison 2 : f() || g()
    printf("Test 2: f() || g()\n");
    if (f() || g()) {
        printf("Condition f() || g() est vraie\n");
    } else {
        printf("Condition f() || g() est fausse\n");
    }
    printf("f_calls: %d, g_calls: %d\n\n", f_calls, g_calls);

    // Combinaison 3 : !f() && g()
    printf("Test 3: !f() && g()\n");
    if (!f() && g()) {
        printf("Condition !f() && g() est vraie\n");
    } else {
        printf("Condition !f() && g() est fausse\n");
    }
    printf("f_calls: %d, g_calls: %d\n\n", f_calls, g_calls);

    // Combinaison 4 : g() && f()
    printf("Test 4: g() && f()\n");
    if (g() && f()) {
        printf("Condition g() && f() est vraie\n");
    } else {
        printf("Condition g() && f() est fausse\n");
    }
    printf("f_calls: %d, g_calls: %d\n\n", f_calls, g_calls);

    // Combinaison 5 : g() || !f()
    printf("Test 5: g() || !f()\n");
    if (g() || !f()) {
        printf("Condition g() || !f() est vraie\n");
    } else {
        printf("Condition g() || !f() est fausse\n");
    }
    printf("f_calls: %d, g_calls: %d\n\n", f_calls, g_calls);

    return 0;
}
