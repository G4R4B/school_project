#!/bin/bash

TEST_DIR="tests_files/bunch_of_tests"
COMPILER="./test_compiler.sh"
LOG_FILE="test_results.log"

echo "Test Results - $(date)" > "$LOG_FILE"
echo "==============================" >> "$LOG_FILE"

dune build
for test_file in "$TEST_DIR"/*.c; do
    echo "Running test: $test_file"
    echo "Test: $test_file" >> "$LOG_FILE"
    
    diff <($COMPILER $test_file) <(./cc.sh $test_file) >> "$LOG_FILE"
    
    if [ $? -eq 0 ]; then
        echo "Result: PASS" >> "$LOG_FILE"
    else
        echo "Result: FAIL" >> "$LOG_FILE"
    fi
    
    echo "------------------------------" >> "$LOG_FILE"
done

rm -r "$TEST_DIR"/*.json
rm -r "$TEST_DIR"/*.s
rm -r "$TEST_DIR"/*.exe

echo "All tests completed. Results are in $LOG_FILE."
