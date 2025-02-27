int f(int x) {
  int y ;
  for (int i = 0; i < 100; i++) {
    x=x+1;
    y=0;
    while(y<10) {
      y = y+1;
    }
    if(x%10 == 0 ) {
      break;
    }
  }
  return x;
}

int main () {
  f(42);
}
