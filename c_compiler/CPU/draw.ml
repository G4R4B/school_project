(* open Circuit
open Libdraw 
   
 let _ =
  let l1 = List.init nb_bits (fun _ -> nouvelle_tension ()) in
  let l2 = List.init nb_bits (fun _ -> nouvelle_tension ()) in
   let a,b = Memory.memoire 1 (nouvelle_tension()) l1 l2 (nouvelle_tension()) (nouvelle_tension()) in
   draw_pdf "/tmp/word_register.pdf" 
   (
     Array.concat([(Array.of_list l1);(Array.of_list l2)])
   )
   
   (Array.concat [a;b])
  *)
