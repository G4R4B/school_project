open Circuit ;;

let neg a = 
    nand a a

let ou a b = 
    nand (neg a) (neg b)
let et a b = 
    neg (nand a b)
let xor a b =
    ou (et a (neg b)) (et (neg a) b)
let mux flag a b =
    let s_neg = neg flag in
    let x1 = et (s_neg) a in (* Select input 1 when flag is 0 *)
    let x2 = et flag b in  (* Select input 2 when flag is 1 *)
    ou x1 x2               (* Output the selected input *)

let demux flag a b =
    let a1 = et flag (et (neg a) (neg b)) in
    let a2 = et flag (et a (neg b)) in
    let a3 = et flag (et (neg a) b) in
    let a4 = et flag (et a b) in
    [|a1; a2; a3; a4|]

let rec pow a = function
    | 0 -> 1
    | 1 -> a
    | n -> 
      let b = pow a (n / 2) in
      b * b * (if n mod 2 = 0 then 1 else a)
let demux_array a n =
    if n > Array.length a then failwith "demux_array: not enough elements";
    if n mod 2 != 0 then failwith "demux_array: n must be even";
    let list_start = demux un a.(n-2) a.(n-1)  in
    if n = 2 then list_start
    else
    let rec demux_rec i list_start =
        if i = 0 then list_start
        else
            let list_start = Array.map (fun x -> demux x a.(i-2) a.(i-1)) list_start in
            demux_rec (i-2) (Array.concat (Array.to_list list_start))
    in
    demux_rec (n-2) list_start

let demux_array_odd_or_even a n =
    if n mod 2 = 0 then demux_array a n
    else 
    let list_start = demux_array a (n-1)
    in
    Array.concat [(Array.map (fun x -> et x (neg(a.(n-1)))) list_start); (Array.map (fun x -> et x a.(n-1)) list_start)]

        
        
    
(* mux renvoie une tension qui vaut celle de a quand flag=0 et celle de b sinon *)


(* Les fonctions suivantes prennent en entrée des tableau *)
let inverse a = 
    Array.map neg a

let selecteur flag a b = 
    Array.map2 (mux flag) a b

let et_logique a b = 
    (* let n = Array.length a in
    let res = Array.make n Circuit.zero in
    for i = 0 to n-1 do
        res.(i) <- et a.(i) b.(i)
    done;
    res *)
    Array.map2 et a b
  
let ou_logique a b = 
    Array.map2 ou a b
let xor_logique a b = 
    Array.map2 xor a b
