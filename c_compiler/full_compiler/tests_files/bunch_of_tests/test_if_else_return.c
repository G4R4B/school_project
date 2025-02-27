#include <stdio.h>

void complex_recursive_function_tests(int depth) {
    if (depth == 0) {
        return;
    }

    int a = depth;
    int b = depth * 2;
    int c = depth + 3;
    int d = depth % 2;

    // Testing recursive function with if-else, both branches with blocks
    if (a % 2 == 0) {
        {
            if (b > 10) {
                {
                    if (c % 3 == 0) {
                        {
                            complex_recursive_function_tests(depth - 1);
                        }
                    } else {
                        {
                            complex_recursive_function_tests(depth - 1);
                        }
                    }
                }
            } else {
                {
                    if (d == 1) {
                        {
                            complex_recursive_function_tests(depth - 1);
                        }
                    } else {
                        {
                            complex_recursive_function_tests(depth - 1);
                        }
                    }
                }
            }
        }
    } else {
        {
            if (b < 20) {
                {
                    if (c % 4 == 0) {
                        {
                            complex_recursive_function_tests(depth - 1);
                        }
                    } else {
                        {
                            complex_recursive_function_tests(depth - 1);
                        }
                    }
                }
            } else {
                {
                    if (d == 0) {
                        {
                            complex_recursive_function_tests(depth - 1);
                        }
                    } else {
                        {
                            complex_recursive_function_tests(depth - 1);
                        }
                    }
                }
            }
        }
    }
}

int main() {
    printf("Testing complex recursive functions with if-else blocks for performance...\n");
    complex_recursive_function_tests(2000);

    return 0;
}
