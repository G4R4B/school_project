{
  open Lexing
  open Parser

  exception Lexing_error of char

  let kwd_tbl = [
    "int", INT; "void", VOID; "char", CHAR;
     "if", IF; "else", ELSE;
    "return", RETURN; "break", BREAK; "continue", CONTINUE;
    "while", WHILE; "for", FOR; "do", DO; "switch", SWITCH; "case", CASE; "default", DEFAULT;
    "NULL", CST "0"; "stderr", CST "2"; "stdin", CST "0"; "stdout", CST "1";
    "sizeof", SIZEOF;
  ]
  let id_or_kwd s = try List.assoc s kwd_tbl with _ -> IDENT s

  let newline lexbuf =
    let pos = lexbuf.lex_curr_p in
    lexbuf.lex_curr_p <- 
      { pos with pos_lnum = pos.pos_lnum + 1; pos_bol = pos.pos_cnum }

  let desescape s =
    let rec foo i =
      if String.length s = i then []
      else if i + 1 < String.length s && s.[i] = '\\' then
        let c = match s.[i + 1] with
          | 'n' -> '\n'
          | 'r' -> '\r'
          | 't' -> '\t'
          | '"' -> '"'
          | c -> raise (Lexing_error c)
        in c :: foo (i + 2)
      else s.[i] :: foo (i + 1)
    in
    foo 0 |> List.map (String.make 1) |> String.concat ""

}

let letter = ['a'-'z' 'A'-'Z' '_']
let digit = ['0'-'9']
let char = [ '\x00' - '\x7f']
let ident = letter (letter | digit)*
let integer = ['0'-'9']+
let newline = ['\n']
let space = [' ' '\t' '\r']+
let chaine = ([^'\"'] | '\\''\n' | '\\''\"')*
let comment = '/''/' [^'\n']*
let import = "#include" space ['<' '\"'] (ident | '.' | '/')+ ['>' '\"']

rule token = parse
  | space        { token lexbuf }
  | newline       { newline lexbuf; token lexbuf }
  | comment       { token lexbuf }
  | ident as id   { [id_or_kwd id] }
  | integer as s  { [CST(s)] }
  | import        { token lexbuf } (* ignore imports for the moment *)
  | '('           { [LPAREN] }
  | ')'           { [RPAREN] }
  | '['           { [LBRACKET] }
  | ']'           { [RBRACKET] }
  | '{'           { [LBRACE] }
  | '}'           { [RBRACE] }
  | ','           { [COMMA] }
  | ';'           { [SEMI] }
  | '='           { [EQ] }
  | '=''='          { [EQQ] }
  | '!''='          { [NEQ] }
  | '&''&'          { [AND] }
  | '&'          { [ADDR] }
  | '|''|'          { [OR] }
  | '!'           { [NOT] }
  | '<'           { [LT] }
  | '<''='          { [LEQ] }
  | '>'           { [GT] }
  | '>''='          { [GEQ] }
  | '+''+'          { [INCR] }
  | '-''-'          { [DECR] }
  | '+'           { [PLUS] }
  | '+''='          { [PLUS_EQ] }
  | '-'           { [MINUS] }
  | '*'           { [TIMES] }
  | '/'           { [DIV] }
  | '%'           { [MOD] }
  | '\'' (char as c) '\'' { [CHARAT( String.make 1 c )] }
  | '\"' (chaine as s) '\"' { [STR(desescape s)] }
  | eof           { [EOF] }
  | _ as c        { raise (Lexing_error c) }

{
  let rec take_buffered = 
    let buffer = ref None in
    fun lexbuf ->
      match !buffer with
      | Some (x::t) -> buffer := Some t ; x
      | Some [] -> buffer := Some (token lexbuf); take_buffered lexbuf
      | None -> buffer := Some (token lexbuf); take_buffered lexbuf
}
