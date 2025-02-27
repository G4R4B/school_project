#include <stdio.h>

void print_int(int a) {
    printf("%d\n", a);
}

int f(){
    printf("%d\n", (1&&0)||(0&&1));
    return 0;
}

int main() {
  print_int(((1&&0)||(0&&1)));
  f();
  return 0;
}