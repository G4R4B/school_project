open Parser
open Lexing
open Lexer
open Printf
open Ast

   
let pos ((s,e):ppos) =
  "pos", `Assoc [ "start_line",`Int s.pos_lnum ;
                 "start_char",`Int (s.pos_cnum-s.pos_bol) ;
                 "end_line",`Int e.pos_lnum ;
                 "end_char",`Int (e.pos_cnum-e.pos_bol) ]
  
   
(* localise une erreur en indiquant la ligne et la colonne *)
let localisation pos =
  let l = pos.pos_lnum in
  let c = pos.pos_cnum - pos.pos_bol + 1 in
  eprintf "À la ligne %d, autour des positions %d-%d:\n"  l (c-1) c;;
  
  
let rec to_json_program p =  `List (List.map to_json_global_stmt p )
and to_json_global_stmt = function
  | GFunDef(name, args, body, p) ->
     `Assoc([
        "type", `String "fundef" ;
        "name", `String name ;
        "args", `List (List.map (fun x-> `String x) args) ;
        "body", to_json_stmt body ;
        pos p
           ])
  | Gstmt(s, p) ->
     `Assoc([
               "type", `String "stmt" ;
               "stmt", to_json_stmt s ;
               pos p
           ])
and to_json_stmt = function
  | Sfor (varname, in_set, body, p) ->
     `Assoc([
        "type", `String "for" ;
        "varname", `String varname ;
        "in_set", to_json_expr in_set ;
        "body", to_json_stmt body ;
        pos p
           ])
  | Sif_else (cond, then_stmt, else_stmt, p) ->
     `Assoc([
               "type", `String "if_else" ;
               "cond", to_json_expr cond ;
               "then", to_json_stmt then_stmt ;
               "else", to_json_stmt else_stmt ;
               pos p
           ])
   | Sif (cond, then_stmt, p) ->
     `Assoc([
               "type", `String "if" ;
               "cond", to_json_expr cond ;
               "then", to_json_stmt then_stmt ;
               pos p
           ])
   | Swhile (cond, body, p) ->
       `Assoc([
                "type", `String "while" ;
                "cond", to_json_expr cond ;
                "body", to_json_stmt body ;
                pos p
             ])
  | Sblock(l,p) ->
     `Assoc([
               "type", `String  "stmt list" ;
               "body", `List (List.map to_json_stmt l) ;
               pos p
           ])
  | Sreturn(e,p) ->
     `Assoc([
               "type", `String  "return" ;
               "value", to_json_expr e ;
               pos p
           ])     
  | Sassign(l, e, p) ->
     `Assoc([
               "type", `String "varset" ;
               "left_value", to_json_left_value l ;
               "value", to_json_expr e ;
               pos p
           ])     
  | Sval (e,p) ->
     `Assoc([
               "type", `String "expr" ;
               "value", to_json_expr e ;
               pos p
           ]) 
   | SYield (e,p) ->
         `Assoc([
                  "type", `String "yield" ;
                  "value", to_json_expr e ;
                  pos p
               ])
   | Break p ->
     `Assoc([
               "type", `String "break" ;
               pos p
           ])
   | Continue p ->
       `Assoc([
                "type", `String "continue" ;
                pos p
             ])
and to_json_expr = function
  | Const(c, p) ->
     `Assoc([
               "type", `String "const" ;
               "value", to_json_const c ;
               pos p
           ]) 
  | Val(lv, p) ->
     `Assoc([
               "type", `String "left_value" ;
               "value", to_json_left_value lv ;
               pos p
           ]) 
  | Moins(e, p) ->
     `Assoc([
               "type", `String "moins" ;
               "value", to_json_expr e ;
               pos p
           ]) 
  | Not(e, p) ->
     `Assoc([
               "type", `String "not" ;
               "value", to_json_expr e ;
               pos p
           ]) 
  | Op(op, e1, e2, p) ->
     `Assoc([
               "type", `String "binop" ;
               "binop", `String (str_op op) ;
               "v1", to_json_expr e1 ;
               "v2", to_json_expr e2 ;
               pos p
           ])
  | List(l, p) ->
     `Assoc([
               "type", `String "list" ;
               "content", `List (List.map to_json_expr l) ;
               pos p
           ])
   | Tuple(l, p) ->
       `Assoc([
                "type", `String "tuple" ;
                "content", `List (List.map to_json_expr l) ;
                pos p
             ])
   | ListFor(e, s, e2, p) ->
       `Assoc([
                "type", `String "list for" ;
                "content", to_json_expr e ;
                "varname", `String s ;
                "in_set", to_json_expr e2 ;
                pos p
             ])
  | Ecall(s, args, p) ->
     `Assoc([
               "type", `String "call" ;
               "funname", `String s ;
               "args", `List (List.map to_json_expr args) ;
               pos p
           ])
   | EcallLeftValue(l, args, p) ->
         `Assoc([
                  "type", `String "call" ;
                  "funname", to_json_left_value l ;
                  "args", `List (List.map to_json_expr args) ;
                  pos p
               ])
and to_json_left_value = function
  | Var(s,p) ->
     `Assoc([
               "type", `String "var" ;
               "name", `String s ;
               pos p
           ])  
  | Tab(l,idx,p) ->
     `Assoc([
               "type", `String "array access" ;
               "array", to_json_left_value l ;
               "index", to_json_expr idx ;
               pos p
           ])
and to_json_const = function
  | Int(i, p) ->
     `Assoc([
               "type", `String "int" ; 
               "value", `Int (int_of_string i) ;
               pos p
           ])   
  | Str(s, p) ->
     `Assoc([
               "type", `String "string" ;
               "value", `String s ;
               pos p
           ])   
  | Bool(b, p) ->
     `Assoc([
               "type", `String "bool" ;
               "value", `Bool b ;
               pos p
           ])   
  | Non(p) ->
     `Assoc([
               "type", `String "none" ;
               pos p
           ])
    


let to_json_safe ifile = 
  let f = open_in ifile in
  let buf = Lexing.from_channel f in
  let res_json =
    try
      let program_ast = file take_buffered buf in
      to_json_program program_ast 
    with
    | Lexer.Lexing_error c -> 
       (* Erreur lexicale. On récupère sa position absolue et 
	on la convertit en numéro de ligne *)
       localisation (Lexing.lexeme_start_p buf);
       eprintf "Erreur dans l'analyse lexicale: %c.\n" c;
       exit 2; (*know error code*)
    | Parser.Error -> 
       (* Erreur syntaxique. On récupère sa position absolue et on la 
	convertit en numéro de ligne *)
       localisation (Lexing.lexeme_start_p buf);
       eprintf "Erreur dans l'analyse syntaxique.\n";
       exit 3; (*know error code*)
    | _ ->
       localisation (Lexing.lexeme_start_p buf);
       eprintf "Une erreur inconnue est intervenue.\n";
       exit 4; (*know error code*)
  in
  close_in f ;
  res_json
