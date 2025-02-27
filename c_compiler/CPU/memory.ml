open Circuit
open Logique

let bit_registre  doit_ecrire valeur_ecrite =
  (*flip flop for just one bit*)
  let nvval = valeur_ecrite in 
  let ancienval = nouvelle_tension () in
  let futurval = mux doit_ecrire ancienval nvval in
  relie ancienval (delai futurval);
  ancienval
  
let word_registre doit_ecrire valeur_ecrite  =
  Array.map (fun x -> bit_registre doit_ecrire x) valeur_ecrite


let split_at_point l n =
  let rec split_rec l n acc =
          if n = 0 then (acc, l)
          else
            match l with
            | [] -> failwith "split_at_point: not enough elements"
            | x::xs -> split_rec xs (n-1) (acc @ [x])
        in
  split_rec l n []
      
let selecteur_array flag a b =
  Array.map2 (fun x y -> selecteur flag x y) a b


let memoire taille_addr set l1 l2 e v =
  let l1 = Array.of_list l1 in
  let l2 = Array.of_list l2 in
  let e = Array.of_list e in
  let decoder_table = demux_array_odd_or_even e (taille_addr) in
  (* print_int (Array.length decoder_table);
  print_newline (); *)
  let output_table = Array.init (pow 2 taille_addr) (fun i -> word_registre (et set decoder_table.(i)) v) in
  let rec find_addr lnow valueuse i =
    let part1, part2 = (split_at_point (Array.to_list valueuse) (Array.length valueuse / 2))
    in
  let out1 = Array.of_list part1 in
  let out2 = Array.of_list part2 in
  let select = selecteur_array lnow.(i) out1 out2 in
  if Array.length out1 = 1 then select.(0)
  else find_addr lnow select (i-1)
in
let valuel1 = find_addr l1 output_table (taille_addr - 1)
in
let value2 = find_addr l2 output_table (taille_addr - 1)
in

let _ = (set, e, v) in
(valuel1, value2)
 

let log2of n =
  let rec log2of_rec n acc =
    if n = 1 then acc
    else log2of_rec (n/2) (acc+1)
  in
  log2of_rec n 0

let rom l1 l2 valeurs =
  let l1 = Array.of_list l1 in
  let l2 = Array.of_list l2 in
  let rec rom_rec lnow valueuse i =
    let part1, part2 = (split_at_point (Array.to_list valueuse) (Array.length valueuse / 2))
    in
    let out1 = Array.of_list part1 in
    let out2 = Array.of_list part2 in
    let select = selecteur_array lnow.(i) out1 out2 in
    if Array.length out1 = 1 then select.(0)
    else rom_rec lnow select (i-1)
  in
  let valuel1 = rom_rec l1 valeurs (log2of (Array.length valeurs) - 1)
  in
  let valuel2 = rom_rec l2 valeurs (log2of (Array.length valeurs) - 1)
in
  (valuel1, valuel2)


let read_program pc valeurs =
    let l1 = pc in
    let rec rom_rec lnow valueuse i =
      let part1, part2 = (split_at_point (Array.to_list valueuse) (Array.length valueuse / 2))
      in
      let out1 = Array.of_list part1 in
      let out2 = Array.of_list part2 in
      let select = selecteur_array lnow.(i) out1 out2 in
      if Array.length out1 = 1 then select.(0)
      else rom_rec lnow select (i-1)
    in
    let valuel1 = rom_rec l1 valeurs (Array.length l1 - 7)
    in
    valuel1




let ram_rom taille_addr set l1 l2 e v contenu_rom =
  (*ram at 256 .. 511 and rom on 0..255*)
  print_int taille_addr;
  let valueraml1, valueraml2 = memoire taille_addr set l1 l2 e v in
  let valueroml1, valueroml2 = rom l1 l2 contenu_rom in
  let l1 = Array.of_list l1 in
  let l2 = Array.of_list l2 in
  let valuel1 = selecteur l1.(taille_addr) valueroml1 valueraml1 in
  let valuel2 = selecteur l2.(taille_addr) valueroml2 valueraml2 in
  (valuel1, valuel2)