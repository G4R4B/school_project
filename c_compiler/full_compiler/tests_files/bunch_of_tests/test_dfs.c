#include <stdio.h>

int adj[10][10];  // Matrice d'adjacence pour représenter le graphe
int visited[10];  // Tableau pour suivre les nœuds visités
int node_count;   // Compteur de nœuds visités dans un parcours DFS

// Initialisation du graphe avec des liens fixes pour la démonstration
void initialize_graph() {
    int i;
    int j;
    for (i = 0; i < 10; i++) {
        for (j = 0; j < 10; j++) {
            if (i + 1 == j || j + 1 == i){
                adj[i][j] = 1;
            } else {
                adj[i][j] = 0;
            }
        }
    }
}

// Parcours en profondeur (DFS) récursif
void dfs(int node) {
    visited[node] = 1;
    node_count++;

    for (int i = 0; i < 10; i++) {
        if (adj[node][i] == 1 && !visited[i]) {
            dfs(i);
        }
    }
}

int main() {
    int total_nodes_visited = 0;

    initialize_graph(); // Initialisation du graphe avec des liens prédéfinis

    for (int i = 0; i < 500; i++) {
        // Réinitialiser les tableaux visités et le compteur pour chaque DFS
        for (int j = 0; j < 10; j++) {
            visited[j] = 0;
        }
        node_count = 0;

        // Exécuter DFS depuis le nœud 0
        dfs(0);

        // Ajouter le nombre de nœuds parcourus à la somme totale
        total_nodes_visited += node_count;
    }

    printf("Nombre total de nœuds parcourus en 500 DFS : %d\n", total_nodes_visited);

    return 0;
}
