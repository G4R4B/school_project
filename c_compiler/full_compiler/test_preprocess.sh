if [ -z "$1" ]; then
    echo "Usage: $0 <test_file>"
    exit 1
fi

TEST_DIR="tests_files"
TO_COMPILE="$1"

./c2json.exe "$TEST_DIR/$TO_COMPILE" &&

python json_preprocess/main.py "$TEST_DIR/${TO_COMPILE%.*}".json