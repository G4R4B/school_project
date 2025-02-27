open Circuit
open Arithmetique
open Cpu
   
let ins_add x y dst =  8+16*(dst+16*(x+16*y))
let ins_moins x y dst =  12+16*(dst+16*(x+16*y))
let ins_et x y dst =  10+16*(dst+16*(x+16*y))
let ins_ou x y dst =  14+16*(dst+16*(x+16*y))
let ins_inv x dst =  9+16*(dst+16*(x+16*0))
let ins_xor x y dst =  13+16*(dst+16*(x+16*y))
let ins_inc x dst =  11+16*(dst+16*(x+16*0))
let ins_dec x dst =  15+16*(dst+16*(x+16*0))
let ins_cst_hi valeur dst = 7+16*(dst+16*(valeur))
let ins_cst_low valeur dst = 6+16*(dst+16*(valeur))
let ins_load reg_adr delta dst =5+16*(dst+16*(reg_adr+16*(if delta < 0 then delta+16 else delta)))
let ins_get_pc dst delta = 4 + 16*(dst+16*(if delta < 0 then delta+256 else delta))
let ins_store reg_adr delta reg_val =3+16*((if delta < 0 then delta+16 else delta)+16*(reg_adr+16*reg_val))
let ins_jump_short delta = 2+64*(delta)
let ins_jump_short_relatif delta = 2+16+64*(if delta < 0 then delta+2048 else delta)
let ins_jump_negatif_relatif reg_cond delta =
  let delta = if delta < 0 then delta+128 else delta in
  1+16+32*(delta mod 8 + 8*(reg_cond+16*(delta/8)))
let ins_jump_est_zero_relatif reg_cond delta =
  let delta = if delta < 0 then delta+64 else delta in
  0+16+64*(delta mod 4 + 4*(reg_cond+16*(delta/4)))
let ins_jump_nonzero_relatif reg_cond delta =
  let delta = if delta < 0 then delta+64 else delta in
  0+16+32+64*(delta mod 4 + 4*(reg_cond+16*(delta/4)))


(*alu test*)
let test = ins_cst_low 0 0;;
let setfirst = ins_cst_low 10 2;;
let setsecond = ins_cst_low 12 1;;
let add = ins_add 1 2 0;;
let sub = ins_moins 1 2 0;; 

(*ram test*)
let store = ins_store 0 0 1;;

let load = ins_load 0 0 3;;

print_endline (string_of_int test);;

let contenu = Array.init 256 (fun i -> (if i=0 then test else if i=1 then setfirst else if i=2 then setsecond else if i=3 then add 
else if i=4 then sub else if i=5 then store else if i=6 then load else load
  ) |> nb_vers_bits |> Array.of_list |> Array.map (function | 0 -> zero | _ -> un))
;;
print_endline (string_of_int test);;


let pc, instruction_fetch, final_value_r1, ramatr2, decoder_table = cpu contenu
;;
print_endline (string_of_int test);;
let out = Array.concat [pc; instruction_fetch; final_value_r1; ramatr2;[|decoder_table|]];;
let s = compile [||] out;;

for i = 0 to 6 do
  print_int i;
  prerr_newline();
  let test = s [||] in
  let pc = Array.sub test 0 8 in
  let instruction_fetch = Array.sub test 8 16 in
  let final_value_r1 = Array.sub test 24 16 in
  let register2 = Array.sub test 40 16 in
  let decoder_table = test.(56) in
  let string_of_int_array a = Array.fold_left (fun acc x -> acc ^ ";" ^ (string_of_int x)) "" a in
  print_endline ("pc: " ^ (string_of_int_array pc) ^ " instruction_fetch: " ^ (string_of_int_array instruction_fetch) );
  print_endline (" final_value_r1: " ^ (string_of_int_array final_value_r1) ^ " R2: " ^ (string_of_int_array register2));
  print_endline (" decoder_table: " ^ (string_of_int decoder_table))
done