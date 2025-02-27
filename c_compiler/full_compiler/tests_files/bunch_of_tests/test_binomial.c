#include <stdio.h>
#include <stdlib.h>

// Fonction de mémoisation pour les coefficients binomiaux
int binomial_memo(int n, int k, int memo[100][100]) {
    if (k == 0 || k == n) { // Cas de base
        return 1;
    }
    if (memo[n][k] != -1) { // Si déjà calculé, retourner le résultat mémorisé
        return memo[n][k];
    }
    // Calculer et mémoriser la valeur
    memo[n][k] = binomial_memo(n - 1, k - 1, memo) + binomial_memo(n - 1, k, memo);
    return memo[n][k];
}

// Initialisation du tableau de mémoisation
int binomial(int n, int k) {
    int memo[100][100];
    for (int i = 0; i <= n; i++) { // Initialisation avec -1 pour indiquer non-calculé
        for (int j = 0; j <= k; j++) {
            memo[i][j] = -1;
        }
    }
    return binomial_memo(n, k, memo);
}

int main() {
    // Calculer et afficher les coefficients binomiaux
    for (int n = 0; n <= 10; n++) {
        for (int k = 0; k <= n; k++) {
            printf("C(%d, %d) = %d\n", n, k, binomial(n, k));
        }
    }

    return 0;
}