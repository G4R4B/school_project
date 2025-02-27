open Logique
open Circuit
open Arithmetique
open Memory
open Alu

(* Initialisation du CPU et de la mémoire *)
let cpu program =
  let zeroarr = Array.init nb_bits (fun _ -> zero) in
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

  let instruction, ramatregister2 = ram_rom 8 futurset_memory (Array.to_list (Array.concat [pc; [|zero|]])) (Array.to_list (Array.concat [(Array.sub register2 0 8); [|un|]])) (Array.to_list futur_adress_to_write) register3 program in

  (* Extraction des différentes parties de l'instruction *)
  let opcode = Array.sub instruction 0 4 in
  let r1 = Array.sub instruction 4 4 in
  let r2 = Array.sub instruction 8 4 in
  let r3 = Array.sub instruction 12 4 in
  Array.iteri (fun i x -> relie r1.(i) x) futurr1;
  Array.iteri (fun i x -> relie r2.(i) x) futurr2;
  Array.iteri (fun i x -> relie r3.(i) x) futurr3;

  (* Decoder pour choisir quelle opération effectuer *)
  let decoder_table = demux_array_odd_or_even opcode 4 in

  (*If R1 need to be written, we need to set the set bit*)
  let memory_set = Array.fold_left (fun acc x -> ou acc x) zero (Array.sub decoder_table 4 12) in
  relie futurset memory_set;
  (* Implémentation des opcodes *)

  (* ALU : Opérations de 8 à 15 *)
  let alu_value = selecteur opcode.(3) zeroarr (alu (Array.sub opcode 0 3) register2 register3) in

  (* Opcode 6 et 7 : Chargement de constantes *)
  let bit_max = selecteur decoder_table.(7) zeroarr (Array.init nb_bits (fun i -> if i < 8 then zero else if i < 12 then r2.(i-8) else r3.(i-12))) in
  let bit_min = selecteur decoder_table.(6) zeroarr (Array.init nb_bits (fun i -> if i < 4 then r2.(i) else if i < 8 then r3.(i-4) else zero)) in

  (* Opcode 5 : Lecture en RAM *)
  let read_r2 = selecteur decoder_table.(5) zeroarr ramatregister2 in

  
  (* Opcode 4 : Jump relatif pc + offset *)
  let pc_extend = Array.concat [pc; Array.init 8 (fun _ -> zero)] in
  let jump_basic = selecteur decoder_table.(4) zeroarr (somme pc_extend (Array.init nb_bits (fun i -> if i < 4 then r1.(i) else if i < 8 then r2.(i-4) else zero))) in

  (* Opcode 3 : Écriture en RAM avec offset *)
  relie decoder_table.(3) futurset_memory;
  let adress_to_write = Array.sub (somme register2 (Array.init 16 (fun i -> if i < 4 then r1.(i) else zero))) 0 8 in
  Array.iteri (fun i x -> relie x futur_adress_to_write.(i)) adress_to_write;

  (* Opcode 2 : Jump inconditionnel relatif *)
  let jump_rel = selecteur decoder_table.(2) zeroarr (somme pc_extend (Array.init nb_bits (fun i -> if i < 2 then r1.(i) else if i < 6 then r2.(i-2) else if i < 10 then r3.(i-6) else zero))) in

  (* Opcode 0 et 1 : Branches conditionnels *)
  let cond1_occured = et (decoder_table.(1)) (xor (est_negatif register2) r1.(0)) in
  let branch_cond1 = selecteur cond1_occured 
      zeroarr
      (selecteur r1.(0) register3 (somme pc_extend (Array.init nb_bits (fun i -> if i < 2 then r1.(i) else if i < 6 then r2.(i-2) else if i < 10 then r3.(i-6) else zero))))
  in
  let cond0_occured = et (decoder_table.(0)) (xor (est_nul register2) r1.(0)) in
  let branch_cond0 = selecteur cond0_occured
      zeroarr
      (selecteur r1.(0) register3 (somme pc_extend (Array.init nb_bits (fun i -> if i < 2 then r1.(i) else if i < 6 then r2.(i-2) else if i < 10 then r3.(i-6) else zero))))
  in

  (* Combiner toutes les valeurs calculées *)
  let all_values_to_set_to_r1 = [|alu_value; bit_max; bit_min; read_r2; jump_basic|] in
  let all_values_to_set_to_pc = [|jump_rel; branch_cond1; branch_cond0|] in

  let final_value_to_r1 = Array.fold_left ou_logique (Array.init nb_bits (fun _ -> zero)) all_values_to_set_to_r1 in
  let new_pc_value = Array.fold_left ou_logique (Array.init nb_bits (fun _ -> zero)) all_values_to_set_to_pc in
  let jump_occured = ou (ou cond0_occured cond1_occured) decoder_table.(2) in

  (* Mettre à jour les valeurs des registres *)
  let new_pc = selecteur jump_occured (increment pc_extend) new_pc_value in
  (* Mettre à jour les valeurs des registres *)
  Array.iteri (fun i x -> relie futurvalue.(i) x) final_value_to_r1;
  Array.iteri (fun i x -> relie pc.(i) (delai x)) (Array.sub new_pc 0 8);

  (* Retourne les valeurs pertinentes pour visualiser ce que fait le CPU *)
  (pc, instruction, final_value_to_r1, ramatregister2, opcode.(3))
;;
