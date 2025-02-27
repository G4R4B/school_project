open Ast
open Yojson

(* Converts position information (ppos) to JSON *)
let pos ((start_pos, end_pos) : ppos) =
  `Assoc [
    "start_line", `Int start_pos.pos_lnum;
    "start_char", `Int (start_pos.pos_cnum - start_pos.pos_bol);
    "end_line", `Int end_pos.pos_lnum;
    "end_char", `Int (end_pos.pos_cnum - end_pos.pos_bol)
  ]

(* Converts binary operators to string *)
let json_binop op =
  `String (match op with
    | Add -> "+"
    | Sub -> "-"
    | Mul -> "*"
    | Div -> "/"
    | Mod -> "%"
    | Eq -> "=="
    | Neq -> "!="
    | Lt -> "<"
    | Leq -> "<="
    | Gt -> ">"
    | Geq -> ">="
    | And -> "&&"
    | Or -> "||")

(* Converts unary operators to string *)
let json_unop op =
  `String (match op with
    | Minus -> "-"
    | PointerValue -> "*"
    | Addr -> "&"
    | Not -> "!"
    | PostIncr -> "++post"
    | PostDecr -> "--post"
    | PreIncr -> "++pre"
    | PreDecr -> "--pre")

(* Converts constants to JSON *)
let to_json_const = function
  | Int (i, p) ->
      `Assoc [ "type", `String "int"; "value", `String i; "pos", pos p ]
  | Str (s, p) ->
      `Assoc [ "type", `String "string"; "value", `String s; "pos", pos p ]
  | Char (c, p) ->
      `Assoc [ "type", `String "char"; "value", `String c; "pos", pos p ]

(* Converts type definitions to JSON *)
let rec to_json_type = function
  | TInt -> `String "int"
  | TVoid -> `String "void"
  | TChar -> `String "char"
  | TPtr t -> `Assoc [ "type", `String "pointer"; "of", to_json_type t ]
  | TTab (t, len) -> `Assoc [ "type", `String "array"; "of", to_json_type t; "len", `String len ]

(* Converts expressions to JSON *)
let rec to_json_expr = function
  | Const (c, p) ->
      `Assoc [ "type", `String "const"; "value", to_json_const c; "pos", pos p ]
  | Var (name, t, p) ->
      `Assoc [ "type", `String "var"; "name", `String name; "var_type", to_json_type t; "pos", pos p ]
  | Tab (name, len, t, values, p) ->
      `Assoc [
        "type", `String "array";
        "name", `String name;
        "len", to_json_expr len;
        "array_type", to_json_type t;
        "values", `List (List.map to_json_expr values);
        "pos", pos p
      ]
  | Tabset (name, index, value, p) ->
      `Assoc [
        "type", `String "array_set";
        "name", `String name;
        "index", to_json_expr index;
        "value", to_json_expr value;
        "pos", pos p
      ]
  | Tabget (name, index, p) ->
      `Assoc [
        "type", `String "array_get";
        "name", `String name;
        "index", to_json_expr index;
        "pos", pos p
      ]
  | Tabget_generic (where, index, p) ->
      `Assoc [
        "type", `String "array_get_generic";
        "where", to_json_expr where;
        "index", to_json_expr index;
        "pos", pos p
      ]
  | Tabset_generic (where, index, value, p) ->
      `Assoc [
        "type", `String "array_set_generic";
        "where", to_json_expr where;
        "index", to_json_expr index;
        "value", to_json_expr value;
        "pos", pos p
      ]
  | Tab_2d (name, len, len2, t, values, p) ->
      `Assoc [
        "type", `String "2d_array";
        "name", `String name;
        "len", to_json_expr len;
        "len2", to_json_expr len2;
        "array_type", to_json_type t;
        "values", `List (List.map to_json_expr values);
        "pos", pos p
      ]
  | Call (name, args, p) ->
      `Assoc [
        "type", `String "call";
        "name", `String name;
        "args", `List (List.map to_json_expr args);
        "pos", pos p
      ]
  | Varget (name, p) ->
      `Assoc [ "type", `String "varget"; "name", `String name; "pos", pos p ]
  | Varset(name, t, value, p) ->
      `Assoc [
        "type", `String "varset";
        "name", `String name;
        "var_type", to_json_type t;
        "value", to_json_expr value;
        "pos", pos p
      ]
  | BinOp (op, lhs, rhs, p) ->
      `Assoc [
        "type", `String "binop";
        "op", json_binop op;
        "lhs", to_json_expr lhs;
        "rhs", to_json_expr rhs;
        "pos", pos p
      ]
  | UnOp (op, e, p) ->
      `Assoc [
        "type", `String "unop";
        "op", json_unop op;
        "expr", to_json_expr e;
        "pos", pos p
      ]
  | Sizeof_type (t, p) ->
      `Assoc [
        "type", `String "sizeof";
        "value", to_json_type t;
        "pos", pos p
      ]
  | Sizeof_expr (e, p) ->
      `Assoc [
        "type", `String "sizeof";
        "value", to_json_expr e;
        "pos", pos p
      ]

(* Converts statements to JSON *)
let rec to_json_stmt = function
  | SExpr (e, p) ->
      `Assoc [ "type", `String "expr_stmt"; "expr", to_json_expr e; "pos", pos p ]
  | Assign_deref (where, value, p) ->
        `Assoc [
          "type", `String "assign_deref";
          "where", to_json_expr where;
          "value", to_json_expr value;
          "pos", pos p
        ]
    | Assign (name, value, p) ->
          `Assoc [
            "type", `String "assign";
            "name", `String name;
            "value", to_json_expr value;
            "pos", pos p
          ]
  | SReturn (e, p) ->
      `Assoc [ "type", `String "return"; "value", to_json_expr e; "pos", pos p ]
  | SBreak p ->
      `Assoc [ "type", `String "break"; "pos", pos p ]
  | SContinue p ->
      `Assoc [ "type", `String "continue"; "pos", pos p ]
  | SIfElse (cond, then_stmt, else_stmt, p) ->
      `Assoc [
        "type", `String "if_else";
        "cond", to_json_expr cond;
        "then", to_json_stmt then_stmt;
        "else", to_json_stmt else_stmt;
        "pos", pos p
      ]
  | SIf (cond, then_stmt, p) ->
      `Assoc [
        "type", `String "if";
        "cond", to_json_expr cond;
        "then", to_json_stmt then_stmt;
        "pos", pos p
      ]
  | SWhile (cond, body, p) ->
      `Assoc [
        "type", `String "while";
        "cond", to_json_expr cond;
        "body", to_json_stmt body;
        "pos", pos p
      ]
  | SDoWhile (body, cond, p) ->
      `Assoc [
        "type", `String "do_while";
        "cond", to_json_expr cond;
        "body", to_json_stmt body;
        "pos", pos p
      ]
  | SFor (init, cond, inc, body, p) ->
      `Assoc [
        "type", `String "for";
        "init", to_json_stmt init;
        "cond", to_json_expr cond;
        "inc", to_json_stmt inc;
        "body", to_json_stmt body;
        "pos", pos p
      ]
  | SBlock (stmts, p) ->
      `Assoc [
        "type", `String "block";
        "body", `List (List.map to_json_stmt stmts);
        "pos", pos p
      ]

(* Converts function parameters to JSON *)
let to_json_param (Param (name, typeof, p)) =
  `Assoc [ "name", `String name; "type", to_json_type typeof; "pos", pos p ]

(* Converts global statements to JSON *)
let to_json_global_stmt = function
  | GFunDef (t, name, params, body, p) ->
      `Assoc [
        "type", `String "function";
        "return_type", to_json_type t;
        "name", `String name;
        "params", `List (List.map to_json_param params);
        "body", `List (List.map to_json_stmt body);
        "pos", pos p
      ]
  | GStmt (stmt, p) ->
      `Assoc [
        "type", `String "stmt";
        "stmt", to_json_stmt stmt;
        "pos", pos p
      ]

(* Converts a full program to JSON *)
let to_json_program (prog : program) =
  `List (List.map to_json_global_stmt prog)

(* Parsing and error handling *)

let to_json_safe (ifile : string) =
  let f = open_in ifile in
  let buf = Lexing.from_channel f in
  let res_json =
    try
      let program_ast = Parser.program Lexer.take_buffered buf in
      to_json_program program_ast
    with
    | Lexer.Lexing_error msg ->
      let pos = Lexing.lexeme_start_p buf in
      Printf.eprintf "Lexical error at line %d: %c\n" pos.pos_lnum msg;
      exit 2
    | Parser.Error ->
      let pos = Lexing.lexeme_start_p buf in
      Printf.eprintf "Syntax error at line %d\n" pos.pos_lnum;
      exit 3
    | _ ->
      let pos = Lexing.lexeme_start_p buf in
      Printf.eprintf "Unknown error at line %d\n" pos.pos_lnum;
      exit 4
  in
  close_in f;
  res_json
