cd interpret_python ;
dune build ;
cd ..
cp interpret_python/ptipython2json.exe .
./ptipython2json.exe file.py
python3 interpret_python/interpreter_of_json/main.py file.json