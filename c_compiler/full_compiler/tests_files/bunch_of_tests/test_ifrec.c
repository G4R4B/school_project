#include <stdio.h>

void print_int(int a) {
  printf("%d\n", a);
}

int llf(int a, int b, int c, int d, int e,
        int f, int g, int h, int i, int j) {
  if(a==0) {
    return 0;
  }
    return a + llf(b,c,d,e,f,g,h,i,j,0);
}

int main () {
  print_int(llf(1,2,3,4,5,6,7,8,9,10));
  return 0;
}