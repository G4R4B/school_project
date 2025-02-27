#include <stdio.h>

// Test AND operator
int test_and(int a, int b) {
    return a && b; // Returns 1 if both a and b are true (non-zero)
}

// Test OR operator
int test_or(int a, int b) {
    return a || b; // Returns 1 if either a or b is true (non-zero)
}

// Test NOT operator
int test_not(int a) {
    return !a; // Returns 1 if a is false (zero)
}

// Global variables to track function calls
int a_calls = 0;
int b_calls = 0;
int c_calls = 0;
int d_calls = 0;

// Function a() with side effect
int a() {
    a_calls++;
    printf("a() called\n");
    return a_calls % 2 == 1; // True on odd calls, false on even
}

// Function b() with side effect
int b() {
    b_calls++;
    printf("b() called\n");
    return b_calls % 3 != 0; // False every third call
}

// Function c() with side effect
int c() {
    c_calls++;
    printf("c() called\n");
    return 1; // Always true
}

// Function d() with side effect
int d() {
    d_calls++;
    printf("d() called\n");
    return 0; // Always false
}

// Combined tests for AND, OR, and NOT
void test_logical_operations() {
    printf("Testing logical operations:\n");

    // Combined expressions
    int a = 20;
    int b = -1;
    int c = 2;
    printf("%d\n",test_and(a, b));
    // (a AND b) OR (NOT c)
    printf("test_or(test_and(a, b), test_not(c)) = %d (Expected: 0)\n", 
           test_or(test_and(a, b), test_not(c)));

    // (a OR b) AND (c NOT)
    printf("test_and(test_or(a, b), test_not(c)) = %d (Expected: 0)\n", 
           test_and(test_or(a, b), test_not(c)));

    // (NOT a) OR (b AND c)
    printf("test_or(test_not(a), test_and(b, c)) = %d (Expected: 0)\n", 
           test_or(test_not(a), test_and(b, c)));

    // ((a OR b) AND NOT (b OR c))
    printf("test_and(test_or(a, b), test_not(test_or(b, c))) = %d (Expected: 0)\n", 
           test_and(test_or(a, b), test_not(test_or(b, c))));
}

int main() {
    test_logical_operations();
        // Reset counters
    a_calls = 0;
    b_calls = 0;
    c_calls = 0;
    d_calls = 0;
    

    // Complex logical expression with &&, ||, and !
    printf("Complex Logical Expression Test:\n");

    int result = (a() && b()) || (!c() && d()) || (a() && (!b() || c()) && d());
    printf("Result of complex expression: %d\n", result);

    // Display the function call counts
    printf("\nFunction call counts:\n");
    printf("a() calls: %d\n", a_calls);
    printf("b() calls: %d\n", b_calls);
    printf("c() calls: %d\n", c_calls);
    printf("d() calls: %d\n", d_calls);
    return 0;
}
