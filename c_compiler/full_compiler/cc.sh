TEST_DIR="."

gcc $TEST_DIR/$1 -o $TEST_DIR/${1%.*}gcc.exe
./$TEST_DIR/${1%.*}gcc.exe

