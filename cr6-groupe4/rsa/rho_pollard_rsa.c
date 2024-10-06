/*
 * Author: Paul Vie
 */
#include <stdio.h>
#include <gmp.h>
#include <stdlib.h>

#pragma GCC optimize("O3,inline")

int main(int argc, char* argv[]){
    if (argc != 2){
        perror("Usage: ./rho_pollard_rsa <n>\n");
        exit(1);
    }
    mpz_t n, x,y,d;
    mpz_init(n);
    mpz_set_str(n, argv[1], 10);
    mpz_init(x);
    mpz_init(y);
    mpz_init(d);
    mpz_set_str(x, "2", 10);
    mpz_set_str(y, "2", 10);
    mpz_set_str(d, "1", 10);
    while(mpz_cmp_ui(d, 1) == 0){
        mpz_mul(x, x, x);
        mpz_add_ui(x, x, 1);
        mpz_mod(x, x, n);
        mpz_mul(y, y, y);
        mpz_add_ui(y, y, 1);
        mpz_mod(y, y, n);
        mpz_mul(y, y, y);
        mpz_add_ui(y, y, 1);
        mpz_mod(y, y, n);
        mpz_sub(d, x, y);
        mpz_gcd(d, d, n);
    }
    printf("d = ");
    mpz_out_str(stdout, 10, d);
    printf("\n");
    printf("n/d = ");
    mpz_divexact(n, n, d);
    mpz_out_str(stdout, 10, n);
    printf("\n");
    return 0;
}
