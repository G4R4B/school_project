TEST_DIR=".."
TO_COMPILE="file.c"

cd full_compiler
dune build

./c2json.exe "$TEST_DIR/$TO_COMPILE" &&

python json_preprocess/main.py "$TEST_DIR/${TO_COMPILE%.*}".json
python json2asm/main.py "$TEST_DIR/${TO_COMPILE%.*}"_preprocess.json
cd $TEST_DIR
rm -f ${TO_COMPILE%.*}.json
rm -f ${TO_COMPILE%.*}_preprocess.json