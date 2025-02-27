#!/bin/bash

TEST_DIR="tests_files"
INTERPRETER="./interpret_file.sh"
LOG_FILE="test_results.log"

echo "Test Results - $(date)" > "$LOG_FILE"
echo "==============================" >> "$LOG_FILE"

dune build
for test_file in "$TEST_DIR"/*.py; do
    echo "Running test: $test_file"
    echo "Test: $test_file" >> "$LOG_FILE"
    
    diff <(./ptipython2json.exe $test_file && python3 interpreter_of_json/main.py "${test_file%.*}".json) <(python3 "$test_file") >> "$LOG_FILE"
    
    if [ $? -eq 0 ]; then
        echo "Result: PASS" >> "$LOG_FILE"
    else
        echo "Result: FAIL" >> "$LOG_FILE"
    fi
    
    echo "------------------------------" >> "$LOG_FILE"
done

rm -r "$TEST_DIR"/*.json

echo "All tests completed. Results are in $LOG_FILE."
