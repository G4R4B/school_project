

#include <stdio.h>

int func1() {
    return 42;
}

void func2() {
}

int func3(int a) {
    return a * 2;
}

char func4(int a, char b, int c) {
    if (a > c) {
        return b;
    } else {
        return 'z';
    }
}

// void func5(int *ptr) {
//     *ptr = 100;
// }

// int func6(int arr[], int len) {
//     int sum = 0;
//     for (int i = 0; i < len; i++) {
//         sum += arr[i];
//     }
//     return sum;
// }

// int* func8(int a) {
//     int* result = &a;
//     return result;
// }

int func9(int a, int b) {
    int result = func3(a) + func3(b);  // Calls func3 twice
    return result;
}

// int func10(int a, int b) { else if not supported
//     if (a == b) {
//         return 1;
//     } else if (a > b) {
//         return 2;
//     } else {
//         return 0;
//     }
// }

void func11(int n) {
    for (int i = 0; i < n; i++) {
        func2();  // Calls a void function in a loop
    }
}

int factorial(int n) {
    if (n <= 1) {
        return 1;
    } else {
        return n * factorial(n - 1);
    }
}

int func12(int a, int b) {
    return func9(func3(a), func3(b));  // Nested function calls
}


int func14(int a, int b) {
    return a + b;
}

char* get_greeting() {
    return "Hello, World!";
}

int func15() {
    int x = 10;
    //return sizeof(x);
}

int sum_of_n(int n) {
    int sum = 0;
    for (int i = 1; i <= n; i++) {
        sum += i;
    }
    return sum;
}

int func16(int a) {
    int sum = 0;
    int i = 0;
    do {
        sum += i;
        i++;
    } while (i <= a);
    return sum;
}

void func18(int a, int b) {
    for (int i = 0; i < a; i++) {
        for (int j = 0; j < b; j++) {
            func2();
        }
    }
}

// Test case 24: Function with a large number of parameters
int func19(int a, int b, int c, int d, int e, int f, int g, int h) {
    return a + b + c + d + e + f + g + h;
}

int func22(int n) {
    int sum = 0;
    for (int i = 0; i < n; i++) {
        if (i == 5) {
            break;
        }
        sum += i;
    }
    return sum;
}

int func23(int n) {
    int sum = 0;
    for (int i = 0; i < n; i++) {
        if (i % 2 == 0) {
            continue;
        }
        sum += i;
    }
    return sum;
}

int func25(int a, int b) {
    int result = func3(a);
    for (int i = 0; i < b; i++) {
        result += func3(i);
    }
    return result;
}

int main(int argc, char** argv) {
    // Test case 1: func1
    printf("func1() = %d\n", func1());

    // Test case 2: func2
    printf("func2(): ");
    func2();  // No return value, just print a message
    printf("Executed func2\n");

    // Test case 3: func3
    printf("func3(10) = %d\n", func3(10));

    // Test case 4: func4
    printf("func4(3, 'x', 5) = %c\n", func4(3, 'x', 5));

    // Test case 7: func7
    // printf("func7(10) = %p\n", func8(10));
    
    // Test case 8: func9
    printf("func9(10, 20) = %d\n", func9(10, 20));

    // Test case 10: func11
    func11(5);

    // Test case 11: factorial
    printf("factorial(5) = %d\n", factorial(5));

    // Test case 12: func12
    printf("func12(10, 20) = %d\n", func12(10, 20));
    // Test case 14: func14
    printf("func14(10, 20) = %d\n", func14(10, 20));

}