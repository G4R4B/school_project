open Logique
open Circuit
open Arithmetique
open Memory

(* Initialisation du CPU et de la mémoire *)
let tiny_cpu program =
  (* Initialisation des registres et affichage du programme *)
  let string_of_tension t = if t = zero then "0" else "1" in
  let string_of_tension_array a = Array.fold_left (fun acc x -> acc ^ ";" ^ (string_of_tension x)) "" a in

  let display_program program =
    Array.iter (fun x -> print_endline (string_of_tension_array x)) program
  in
  display_program program;

  (* PC et registres *)
  let pc = Array.init 8 (fun _ -> nouvelle_tension()) in
  let futurvalue = Array.init nb_bits (fun _ -> nouvelle_tension()) in
  let futurset = nouvelle_tension() in
  let futurr1 = Array.init 4 (fun _ -> nouvelle_tension()) in
  let futurr2 = Array.init 4 (fun _ -> nouvelle_tension()) in
  let futurr3 = Array.init 4 (fun _ -> nouvelle_tension()) in
  let register2, register3 = memoire 4 futurset (Array.to_list futurr2) (Array.to_list futurr3) (Array.to_list futurr1) futurvalue in

  (* Lecture de l'instruction *)
  let futurset_memory = nouvelle_tension() in
  let futur_adress_to_write = Array.init 8 (fun _ -> nouvelle_tension()) in

  let instruction, _ = ram_rom 8 futurset_memory (Array.to_list (Array.concat [pc; [|zero|]])) (Array.to_list (Array.concat [(Array.sub register2 0 8); [|un|]])) (Array.to_list futur_adress_to_write) register3 program in

  (* Extraction des différentes parties de l'instruction *)
  let opcode = Array.sub instruction 0 4 in
  let r1 = Array.sub instruction 4 4 in
  let r2 = Array.sub instruction 8 4 in
  let r3 = Array.sub instruction 12 4 in
  Array.iteri (fun i x -> relie futurr1.(i) x) r1;
  Array.iteri (fun i x -> relie futurr2.(i) x) r2;
  Array.iteri (fun i x -> relie futurr3.(i) x) r3;

  (* Decoder pour choisir quelle opération effectuer *)
  let decoder_table = demux_array_odd_or_even opcode 4 in

  (* Implémentation des opcodes *)
  let memory_set = Array.fold_left (fun acc x -> ou acc x) zero (Array.sub decoder_table 4 12) in
  relie futurset memory_set;

  (* ALU : Opérations de 8 à 15 *)
  let bit_min = (Array.concat [r2; r3; Array.init 8 (fun _ -> zero)]) in


  let final_value_to_r1 = bit_min in
  (* let _ = Array.fold_left ou_logique (Array.init nb_bits (fun _ -> zero)) all_values_to_set_to_pc in
  let _ = ou (ou cond0_occured cond1_occured) decoder_table.(2) in *)

  (* Mettre à jour les valeurs des registres *)
  let pc_extend = Array.concat [pc; Array.init 8 (fun _ -> zero)] in
  let new_pc = (increment pc_extend) in
  (* Mettre à jour les valeurs des registres *)
  Array.iteri (fun i x -> relie futurvalue.(i) x) final_value_to_r1;
  Array.iteri (fun i x -> relie pc.(i) (delai x)) (Array.sub new_pc 0 8);

  (* Retourne les valeurs pertinentes pour visualiser ce que fait le CPU *)
  (pc, instruction, final_value_to_r1, register2, decoder_table.(6))
;;
