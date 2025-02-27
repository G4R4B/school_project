open Logique
open Arithmetique
open Circuit


let alu instruction x y = (* instruction sur 3 bits et x y de 16 bits chacun *)
  (* decoder on all instructions *)
  let a,b,c = instruction.(0), instruction.(1), instruction.(2) in
  let decoder_table = demux_array_odd_or_even [|c;b;a|] 3 in
  let zeroarr = Array.init nb_bits (fun _ -> zero) in
  let operation_table = [|somme; difference; et_logique; ou_logique; (fun x _ -> inverse x); xor_logique; (fun x _ -> increment x); (fun x _ -> decrement x)|] in
  let allresult = Array.init 8 (fun i -> selecteur decoder_table.(i) zeroarr (operation_table.(i) x y)) in
  let res = Array.fold_left (fun acc x -> ou_logique acc x) zeroarr allresult in
  res