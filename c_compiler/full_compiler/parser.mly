%{
  open Ast;;
%}

%token <string> CST
%token <string> CHARAT
%token <string> STR
%token <string> IDENT
%token INT VOID CHAR
%token IF ELSE RETURN SIZEOF
%token WHILE FOR DO SWITCH CASE DEFAULT BREAK CONTINUE
%token EOF SEMI
%token LPAREN RPAREN LBRACE RBRACE LBRACKET RBRACKET
%token COMMA
%token PLUS MINUS TIMES DIV MOD ADDR
%token INCR DECR PLUS_EQ // MINUS_EQ TIMES_EQ DIV_EQ MOD_EQ
%token EQ EQQ NEQ
%token LT LEQ GT GEQ
%token AND OR NOT

/* Define operator precedence and associativity */


%right EQ
%left AND OR           // Opérateurs logiques
%left LT LEQ GT GEQ EQQ NEQ    // Opérateurs de comparaison
%left PLUS MINUS       // Addition et soustraction
%left TIMES DIV MOD    // Multiplication, division, et modulo
%right INCR DECR       // Incrément et décrément (associatif à droite)
%right DEREF  // Précédence pour le déréférencement


%nonassoc LOWER_THAN_ELSE
%nonassoc ELSE

%nonassoc NOT
%nonassoc ADDR /* For address */

%right uminus /* For unary minus */

/* Start point of the grammar */
%start program

/* Type of the values returned by the parser */
%type <Ast.program> program

%%

/* C program structure */
program:
  | global_stmt_list EOF { $1 }
;

global_stmt_list:
  | global_stmt global_stmt_list { $1 :: $2 }
  | /* empty */ { [] }
;

global_stmt:
  | typeof = type_def name = IDENT LPAREN args = param_list RPAREN LBRACE body = stmt_list RBRACE { GFunDef(typeof, name, args, body, $loc) }
  | stmt { GStmt($1, $loc) }
;

type_def:
  | INT { TInt }
  | VOID { TVoid }
  | CHAR { TChar }
  | t = type_def TIMES { TPtr(t) }
  | t = type_def LBRACKET len = CST RBRACKET { TTab(t, len) }


param_list:
  | param param_list_tail { $1 :: $2 }
  | /* empty */ { [] }
;

param_list_tail:
  | COMMA param param_list_tail { $2 :: $3 }
  | /* empty */ { [] }
;

param:
  | typeof = type_def name = IDENT { Param(name, typeof, $loc) }
  | typeof = type_def name = IDENT LBRACKET RBRACKET { Param(name, TPtr(TPtr(typeof)), $loc) }
  | typeof = type_def name = IDENT LBRACKET RBRACKET LBRACKET RBRACKET { Param(name, TPtr(TPtr(TPtr(typeof))), $loc) }
  | typeof = type_def name = IDENT LBRACKET first_len = CST RBRACKET LBRACKET second_len = CST RBRACKET { Param(name, TPtr(TTab(TTab(typeof, second_len), first_len)), $loc) }
  
;

/* Statements */
stmt_list:
  | stmt stmt_list { $1 :: $2 }
  | /* empty */ { [] }
;

stmt:
  | expr_stmt SEMI { $1 }
  | RETURN SEMI { SReturn(Const(Int("0", $loc), $loc), $loc) }
  | RETURN expr SEMI { SReturn($2, $loc) }
  | BREAK SEMI { SBreak($loc) }
  | CONTINUE SEMI { SContinue($loc) }
  | IF LPAREN expr RPAREN stmt ELSE stmt { SIfElse($3, $5, $7, $loc) }
  | IF LPAREN expr RPAREN stmt %prec LOWER_THAN_ELSE { SIf($3, $5, $loc) }
  | WHILE LPAREN expr RPAREN stmt { SWhile($3, $5, $loc) }
  | DO todo = stmt WHILE LPAREN whiletime = expr RPAREN SEMI { SDoWhile(todo, whiletime, $loc) }
  | FOR LPAREN init = expr_stmt SEMI cond = expr SEMI inc = expr_stmt RPAREN inloop = stmt { SFor(init, cond, inc, inloop, $loc) }
  | LBRACE stmt_list RBRACE { SBlock($2, $loc) }
;

/* Expressions */
expr_stmt:
  | TIMES expr EQ value = expr { Assign_deref($2, value, $loc) }
  | name = IDENT EQ value = expr { Assign(name, value, $loc) }
  | name = IDENT PLUS_EQ value = expr { Assign(name, BinOp(Add, Varget(name, $loc), value, $loc), $loc) }
  | expr { SExpr($1, $loc) }
;
expr:
  | i = const_expr { i }
  | name = IDENT { Varget(name, $loc) }
  | typeof = type_def name = IDENT { Var(name, typeof, $loc) }
  | typeof = type_def name = IDENT EQ value = expr { Varset(name, typeof, value, $loc) }


  | name = IDENT LBRACKET index = expr RBRACKET EQ value = expr { Tabset(name, index, value, $loc) }
  | name = IDENT LBRACKET index = expr RBRACKET { Tabget(name, index, $loc) }
  | name = IDENT LBRACKET index = expr RBRACKET LBRACKET index2 = expr RBRACKET { Tabget_generic(Tabget(name, index, $loc), index2, $loc) }
  | name = IDENT LBRACKET index = expr RBRACKET LBRACKET index2 = expr RBRACKET EQ value = expr { Tabset_generic(Tabget(name, index, $loc), index2, value, $loc) }
  | typeof = type_def name = IDENT LBRACKET len = expr RBRACKET LBRACKET len2 = expr RBRACKET { Tab_2d(name, len, len2, typeof, [], $loc) }
  | typeof = type_def name = IDENT LBRACKET len = expr RBRACKET EQ LBRACE value = separated_list(COMMA,expr) RBRACE { Tab(name, len, typeof, value, $loc) }
  | typeof = type_def name = IDENT LBRACKET len = expr RBRACKET EQ value = expr { Tab(name, len, typeof, [value], $loc) }
  | typeof = type_def name = IDENT LBRACKET len = expr RBRACKET { Tab(name, len, typeof, [], $loc) }

  | SIZEOF LPAREN type_def RPAREN { Sizeof_type($3, $loc) }
  | SIZEOF LPAREN expr RPAREN { Sizeof_expr($3, $loc) }
  | name = IDENT LPAREN args = separated_list(COMMA,expr) RPAREN { Call(name, args, $loc) }

  | TIMES expr %prec DEREF { UnOp(PointerValue, $2, $loc) }
  | expr INCR { UnOp(PostIncr, $1, $loc) }
  | expr DECR { UnOp(PostDecr, $1, $loc) }
  | INCR expr { UnOp(PreIncr, $2, $loc) }
  | DECR expr { UnOp(PreDecr, $2, $loc) }
  | ADDR expr { UnOp(Addr, $2, $loc) }
  | lhs = expr binop = op rhs = expr { BinOp(binop, lhs, rhs, $loc) }
  | MINUS expr %prec uminus { UnOp(Minus, $2, $loc) }
  | NOT expr { UnOp(Not, $2, $loc) }
  | LPAREN expr RPAREN { $2 }
;

const_expr:
  | CST { Const(Int($1, $loc), $loc) }
  | STR { Const(Str($1, $loc), $loc) }
  | CHARAT { Const(Char($1, $loc), $loc) }
;

%inline op:
  | PLUS { Add }
  | MINUS { Sub }
  | TIMES { Mul }
  | DIV { Div }
  | MOD { Mod }
  | EQQ { Eq }
  | NEQ { Neq }
  | LT { Lt }
  | LEQ { Leq }
  | GT { Gt }
  | GEQ { Geq }
  | AND { And }
  | OR { Or }
;