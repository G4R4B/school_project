#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <gmp.h>
#include <stdbool.h>
#include <assert.h>
#include "hashmap.h"
#include <string.h>


#pragma GCC optimize("Ofast,inline")
typedef struct pair{
    mpz_t g_k_t;
    unsigned long long k;

} pair;

int pair_compare(const void *a, const void *b, void *udata) {
    const struct pair *ua = a;
    const struct pair *ub = b;
    return mpz_cmp(ua -> g_k_t, ub -> g_k_t);
}

uint64_t pair_hash(const void *item, uint64_t seed0, uint64_t seed1) {
    const struct pair *g_k = item;
    char * g_k_str = mpz_get_str(NULL, 10, g_k -> g_k_t);
    uint64_t hash = hashmap_sip(g_k_str, strlen(g_k_str), seed0, seed1);
    free(g_k_str);
    return hash;
}

int main(int argc, char* argv[]){
    if (argc != 4 && argc != 2){
        perror("Usage: ./bsgs <A> <p> <g>\n ./bsgs <file>\n");
        exit(1);
    }
    mpz_t A; mpz_t p;
    mpz_t g; mpz_t a;
    mpz_init(A); mpz_init(p);
    mpz_init(g); mpz_init(a);
    mpz_set_ui(a, 0);
    mpz_t c; mpz_t inverse;
    mpz_init(c); mpz_init(inverse);
    if (argc == 2){
        FILE* file = fopen(argv[1], "r");
        if (file == NULL){
            perror("File not found\n");
            exit(1);
        }
        char *line = malloc(1024*sizeof(char));
        size_t read = 1024;
        getline(&line, &read, file);
        printf("A = %s\n", line);
        mpz_set_str(A, line, 10);
        getline(&line, &read, file);
        printf("p = %s\n", line);
        mpz_set_str(p, line, 10);
        mpz_set_str(inverse, line, 10);
        getline(&line, &read, file);
        printf("g = %s\n", line);
        mpz_set_str(g, line, 10);
        getline(&line, &read, file);
        printf("a = %s\n", line);
        mpz_set_str(a, line, 10);
        free(line);
    }
    else{
        mpz_set_str(A, argv[1], 10);
        mpz_set_str(p, argv[2], 10);
        mpz_set_str(g, argv[3], 10);
        mpz_set_str(inverse, argv[2], 10);
    }
    mpz_sub_ui(inverse, inverse, 2); // p-2 for Fermat's theorem
    mpz_t m;
    mpz_init(m);
    mpz_sub_ui(p, p, 1); // phi(p) = p-1
    mpz_sqrt(m, p);
    mpz_add_ui(p, p, 1); 
    unsigned long long t = mpz_get_ui(m);
    printf("Baby step\n");
    struct hashmap *map = hashmap_new(sizeof(struct pair), t, 0, 0, pair_hash, pair_compare, NULL, NULL);

    for(unsigned long long i = 0; i < t; i++){
        pair baby;
        mpz_init(baby.g_k_t);
        mpz_powm_ui(baby.g_k_t, g, i, p);
        baby.k = i;
        hashmap_set(map, &baby);
    }
    printf("Baby step done\n");
    //giant precomputation
    mpz_t temp;
    mpz_init(temp);
    mpz_mul(temp, m, inverse); // m*(p-2)
    mpz_powm(c, g, temp, p); // c = g^(m*(p-2)) soit c est l'inverse de g^(m) mod p (théorème de Fermat)
    mpz_clear(temp);
    mpz_clear(inverse);
    mpz_t saveA;
    mpz_init(saveA);
    mpz_set(saveA, A);
    printf("Giant step\n");
    for (unsigned long long i = 0; i < t; i++){
        pair baby_A;
        mpz_init(baby_A.g_k_t);
        mpz_set(baby_A.g_k_t, A);
        const pair *baby = hashmap_get(map, &baby_A);
        mpz_clear(baby_A.g_k_t);
        if (baby != NULL){
            mpz_t temp;
            mpz_init(temp);
            mpz_mul_ui(temp, m, i);
            mpz_add_ui(temp, temp, baby -> k);
            gmp_printf("a = %Zd\n", temp);
            if (mpz_get_d (a) != 0){
                if (mpz_cmp(temp, a) != 0){
                    
                    printf("g^a = "); 
                    mpz_powm(temp, g, temp, p);
                    mpz_out_str(stdout, 10, temp);
                    if (mpz_cmp(temp, saveA) == 0){
                        printf(" Success but another a was found\n");
                    }
                    else{
                        printf(" Error\n");
                    }

                    printf("\n");
                }
            }
            mpz_clear(temp);
            break;
        }
        mpz_mul(A, A, c);
        mpz_mod(A, A, p);
    }
    mpz_clear(A);
    mpz_clear(p);
    mpz_clear(g);
    mpz_clear(a);
    mpz_clear(c);
    mpz_clear(m);
    mpz_clear(saveA);
    //free the hashmap and the mpz_t in the map
    size_t i = 0;
    void *item;
    while(hashmap_iter(map, &i, &item)){
        pair *g_k = item;
        mpz_clear(g_k -> g_k_t);
    }
    hashmap_free(map);
    return 0;
    
}