#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <gmp.h>
#include <stdbool.h>
#include <assert.h>
#include <string.h>


#pragma GCC optimize("Ofast,inline")
/*
def miller_rabin(n):
    p = n-1
    s = 0
    while p % 2 == 0:
        p = p // 2
        s += 1
    for _ in range(50):
        a = random.randint(2, n-1)
        x = pow(a, p, n)
        if x == 1 or x == n-1:
            continue
        for _ in range(s-1):
            x = pow(x, 2, n)
            if x == n-1:
                break
        else:
            return False
    return True
*/
// https://github.com/csknk/fast-modular-exponentiation/blob/master/cpp/main.cpp
void mod_exp_fast(mpz_t result, mpz_t b_in, mpz_t e_in, mpz_t m) {
    mpz_t b, e;
    mpz_init(b);
    mpz_init(e);
    mpz_set(b, b_in);
    mpz_set(e, e_in);

    if (mpz_odd_p(e) != 0) {
        mpz_set(result, b);
    } else {
        mpz_set_ui(result, 1);
    }

    while (mpz_cmp_ui(e, 0) > 0) {
        gmp_printf("mod_exp e=%d\n", mpz_sizeinbase(e, 2));
        mpz_powm_ui(b, b, 2, m);
        mpz_fdiv_q_2exp(e, e, 1);
        if (mpz_odd_p(e) != 0) {
            mpz_mul(result, result, b);
            mpz_mod(result, result, m);
        }
    }
    mpz_clear(b);
    mpz_clear(e);
}

int main(){
    mpz_t p; mpz_t s;
    mpz_t p_save; mpz_t a;
    mpz_t x; mpz_t n;
    mpz_init(p); mpz_init(s);
    mpz_init(p_save); mpz_init(a);
    mpz_init(x); mpz_init(n);
    //try malloc size=18085756944
    char * test = malloc(18085756944);
    memset(test, 0, 18085756944);
    free(test);

    //compute 2**282589933-1
    mpz_ui_pow_ui(n, 2, 282589933);
    mpz_sub_ui(n, n, 1);
    mpz_set_ui(s, 0);
    printf("Finish computing 2**282589933-1\n");
    mpz_set(p, n);
    printf("Finish setting p\n");
    mpz_sub_ui(p, p, 1);
    //save p here
    gmp_randstate_t gmp_randstate_state;
    gmp_randinit_default(gmp_randstate_state);
    mpz_set(p_save, p);
    printf("Start computing\n");
    while (mpz_even_p(p)){
        mpz_fdiv_q_ui(p, p, 2);
        mpz_add_ui(s, s, 1);
    }
    printf("Finish 2**282589933-1 = 2^sd + 1\n");
    for (int i = 0; i < 50; i++){
        mpz_urandomm(a, gmp_randstate_state, p_save);
        printf("Random a\n");
        mpn_powm(x, a, p, n);
        printf("Finish powm\n");
        if (mpz_cmp_ui(x, 1) == 0 || mpz_cmp(x, p_save) == 0){
            continue;
        }
        for (int j = 0; j < mpz_get_ui(s)-1; j++){
            mpz_powm_ui(x, x, 2, n);
            if (mpz_cmp(x, p_save) == 0){
                break;
            }
        }
        printf("False\n");
        return 0;
    }
    printf("True\n");
    return 0;
}