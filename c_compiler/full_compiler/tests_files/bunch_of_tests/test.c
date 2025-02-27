#include <stdio.h>
int z;
char* str;
char rg;
int x = 1 + 2 * 3;
int y = 2;
void* ptr = &x;
char* str = "Hello";
int x;
char c = 'c';
int arr[3] = {1, 2, 30};
int h() {
    { int x ; x = 42 ; }
    return 0;
}
void print_int(int a) {
    printf("%d\n", a);
}

void print_char(char a) {
    printf("%c\n", a);
}

void print_string(char* a) {
    printf("%s\n", a);
}

int main(int argc, char** argv) {
    // printf("%c\n", *str+2);
    // printf("%d\n", x);
    // printf("%d\n", y);
    // printf("%p\n", ptr);
    // printf("%s\n", str);
    // printf("%c\n", c);
    int a = 1;
    int b = 2;
    if (a > b) {
        print_int(a);
    } else {
        print_int(b);
    }
    print_int(a+b*10);
    print_string(str);
    printf("%d\n", x);
    char* str = "Hello2";
    int arr[3] = {1, 2, x};
    printf("%s\n", str);
    printf("%d\n", arr[0]);
    // printf("%s\n", str2);
    // printf("%d\n", arr[0]);
    for (int i = 0; i < 5; i=i+1) {
        a = 0;
        for (int j = 0; j < 50; j=j+1) {
            a = a+j;
            printf("%d\n", a);
            if (a > 20) {
                break;
            }else{
                continue;
            }
            printf("Can't reach here\n");
        }
    }
    // printf("%d\n", arr[0]);
    // printf("%d\n", arr[1]);
    // printf("%d\n", arr[2]);
    // printf("%d\n", h());
    // if (1 != (1+a)) {
    //     return 0 + 1;
    // } else {
    //     return 1 * 2;
    // }

    return 0;
}