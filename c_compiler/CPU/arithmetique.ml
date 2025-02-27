open Circuit
open Logique

let vers_bus b =
  Array.init nb_bits (fun i -> if i=0 then b else zero)

let half_adder a b =
    let sum = xor a b in        (* Sum is XOR of A and B *)
    let carry = et a b in       (* Carry is AND of A and B *)
    (carry, sum)
  let tension_vers_entier x = (* Define the function or import it from the appropriate module *)
    (* Placeholder implementation *)
    if x = zero then 0 else 1
let full_adder a b c =
    let carry1, sum1 = half_adder a b in
    let carry2, sum2 = half_adder sum1 c in
    let carry = ou carry2 carry1 in
    (carry, sum2)
let somme a b =
    let rec somme_rec a b c i =
      if i = nb_bits
      then []
      else
        let carry, sum = full_adder a.(i) b.(i) c in
        sum :: somme_rec a b carry (i+1)
    in
    Array.of_list (somme_rec a b zero 0)


let increment a =
  somme a (vers_bus (un))
let decrement a =
  inverse(increment(inverse a))
  

let difference a b =
  inverse(somme(inverse a) b)

let est_nul a =
  (inverse a) |> Array.fold_left et un

let est_negatif a =
  a.(nb_bits-1)

let est_positif a =
  neg (est_negatif a)

  
let rec bit_liste_vers_nb = (* Suppose le petit-boutisme*)
  function 
  | [] -> 0
  | a::q -> a+2*(bit_liste_vers_nb q)


let nb_vers_bits n = (* Suppose le petit-boutisme *)
  let n = if n < 0 then n + 65536 else n in
  let rec foo n b =
    if b = 0
    then []
    else (n mod 2)::(foo (n/2) (b-1))
  in
  foo n nb_bits
  
let nb_to_array i = ((i+65536) mod 65536) |> nb_vers_bits |> Array.of_list

