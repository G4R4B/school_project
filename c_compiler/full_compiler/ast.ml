(* Syntax tree for a simple C-like language *)

type ppos = Lexing.position * Lexing.position

(* Program: A list of global statements (function definitions or standalone statements) *)
type program = global_stmt list

(* Global statements: Function definitions or standalone statements *)
and global_stmt =
  | GFunDef of type_def * string * param list * stmt list * ppos
  | GStmt of stmt * ppos

(* Function parameters *)
and param = Param of string * type_def * ppos

(* Type definitions *)
and type_def =
  | TInt
  | TVoid
  | TChar
  | TPtr of type_def  (* Pointer type *)
  | TTab of type_def * string  (* Array type *) (*is just for argument passing*)

(* Statements: Various types of statements *)
and stmt =
  | SExpr of expr * ppos                    (* Expression statement *)
  | Assign_deref of expr * expr * ppos    (* Dereference assignment *)
  | Assign of string * expr * ppos          (* Assignment *)
  | SReturn of expr * ppos                  (* Return statement *)
  | SBreak of ppos                          (* Break statement *)
  | SContinue of ppos                       (* Continue statement *)
  | SIfElse of expr * stmt * stmt * ppos    (* If-Else statement *)
  | SIf of expr * stmt * ppos               (* If statement without else *)
  | SWhile of expr * stmt * ppos            (* While loop *)
  | SDoWhile of stmt * expr * ppos          (* Do-While loop *)
  | SFor of stmt * expr * stmt * stmt * ppos (* For loop *)
  | SBlock of stmt list * ppos              (* Block of statements *)

(* Expressions: Represent various kinds of expressions *)
and expr =
  | Const of const * ppos                   (* Constants: integers or strings *)
  | Var of string * type_def * ppos         (* Variable reference with type *)
  | Varget of string * ppos                 (* Variable get *)
  | Varset of string * type_def * expr * ppos (* Variable reference with assignment *)
  | Tab of string * expr * type_def * expr list * ppos (* Array create *)
  | Tabset of string * expr * expr * ppos   (* Array set *)
  | Tabget of string * expr * ppos          (* Array get *)
  | Tabget_generic of expr * expr * ppos    (* Array get *)
  | Tabset_generic of expr * expr * expr * ppos (* Array set *)
  | Tab_2d of string * expr * expr * type_def * expr list * ppos (* 2D array create *)

  | Call of string * expr list * ppos       (* Function call *)
  | BinOp of binop * expr * expr * ppos     (* Binary operations *)
  | UnOp of unop * expr * ppos              (* Unary operations *)
  | Sizeof_type of type_def * ppos          (* Sizeof type *)
  | Sizeof_expr of expr * ppos              (* Sizeof expression *)

(* Constants: Integer and string literals *)
and const =
  | Int of string * ppos
  | Str of string * ppos
  | Char of string * ppos

(* Binary operators *)
and binop =
  | Add
  | Sub
  | Mul
  | Div
  | Mod
  | Eq
  | Neq
  | Lt
  | Leq
  | Gt
  | Geq
  | And
  | Or

(* Unary operators *)
and unop =
  | Minus
  | PointerValue
  | PostIncr
  | PostDecr
  | PreIncr
  | PreDecr
  | Addr
  | Not

(* Utility functions to convert binary and unary operators to strings *)
let str_binop = function
  | Add -> "+"
  | Sub -> "-"
  | Mul -> "*"
  | Div -> "/"
  | Mod -> "%"
  | Eq  -> "=="
  | Neq -> "!="
  | Lt  -> "<"
  | Leq -> "<="
  | Gt  -> ">"
  | Geq -> ">="
  | And -> "&&"
  | Or  -> "||"

let str_unop = function
  | Minus -> "-"
  | PointerValue -> "*"
  | Addr -> "&"
  | Not -> "!"
  | PostIncr -> "++post"
  | PostDecr -> "--post"
  | PreIncr -> "++pre"
  | PreDecr -> "--pre"
