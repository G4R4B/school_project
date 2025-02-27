
# Project Overview

This project consists of three main components: a C compiler, a Python interpreter, and a CPU implementation in OCaml. Each component is designed to demonstrate different aspects of programming language theory and computer architecture.

## C Compiler

The C compiler is responsible for translating C source code into assembly language. It includes several stages such as lexical analysis, syntax analysis, semantic analysis, optimization, and code generation. The main components of the C compiler are:

- **Lexer**: Tokenizes the input C code.
- **Parser**: Builds an abstract syntax tree (AST) from the tokens.
- **Semantic Analyzer**: Checks for semantic errors and annotates the AST.
- **Optimizer**: Performs optimizations on the intermediate representation.
- **Code Generator**: Generates assembly code from the optimized AST.
- **Assembly Optimizations**: Applies optimizations to the generated assembly code.

### Key Files
Two directories contain the main components of the C compiler:
- `full_compiler/json_preprocess/`: Contains the semantic analyzer and optimizer.
- `full_compiler/json2asm/`: Contains the code generator and assembly optimizations.

## Python Interpreter

The Python interpreter executes Python code by parsing it into an intermediate representation and then interpreting that representation.

### Key Files
- `interpret_python/interpreter_of_json/interpreter.py`: Contains the main interpreter logic, including function definitions, variable handling, and expression evaluation.

## CPU Implementation in OCaml

The CPU implementation simulates a simple CPU using OCaml. It includes components for memory management, arithmetic operations, and instruction decoding. The CPU can execute a predefined set of instructions and update its state accordingly.
