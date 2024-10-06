open Quoridor.Board
open Quoridor.Types
let color_to_final_pos color = match color with
  | Red -> ('y',16) (*16 en y*)
  | Blue -> ('y',0) (*0 en y*)
  | Green -> ('x', 16) (*16 en x*)
  | Yellow -> ('x', 0) (*0 en x*)
  
let have_all_player_in_board () =
  let rec aux (i,j) acc = match (i,j) with
    | (16,16) -> acc
    | (i,16) -> if (is_player (i,j)) then aux (i+2,0) ((i,j)::acc)
      else aux (i+2,0) acc
    | (i,j) -> if (is_player (i,j)) then aux (i,j+2) ((i,j)::acc)
      else aux (i,j+2) acc
  in aux (0,0) []

(*
   
let have_all_wall () =
  let rec aux (i,j) acc = match (i,j) with
    | (16,16) -> acc
    | (i,16) -> if (is_wall (i,j)) then aux (i+1,0) ((i,j)::acc)
      else aux (i+1,0) acc
    | (i,j) -> if (is_wall (i,j)) then aux (i,j+1) ((i,j)::acc)
      else aux (i,j+1) acc
  in aux (0,0) []
  
  *)

let test_wall_y pos = 
  match pos with 
  | (x,y) -> 
    try (validate_wall_placement (current_player ()) (x,y) (x,y+1)); Some ((x,y),(x,y+1)) with
    | InvalidWallPlacement (_,_,_) -> None
  | _ -> None
let test_wall_x pos = 
  match pos with 
  | (x,y) -> 
    try validate_wall_placement (current_player ()) (x,y) (x+1,y); Some ((x,y),(x+1,y)) with
    | InvalidWallPlacement (_,_,_) -> None
  | _ -> None

let list_of_wall () =
  let rec aux (i,j) acc = match (i,j) with 
    | (16,16) -> acc
    | (i,16) -> (match (test_wall_y (i,j) , test_wall_x (i,j)) with
    | (Some a, Some b) -> aux (i+1,0) (a::b::acc)
    | (Some a, None) -> aux (i+1,0) (a::acc)
    | (None, Some b) -> aux (i+1,0) (b::acc)
    | (None, None) -> aux (i+1,0) acc
    )
    | (i,j) -> (
        match (test_wall_y (i,j) , test_wall_x (i,j)) with
        | (Some a, Some b) -> aux (i,j+1) (a::b::acc)
        | (Some a, None) -> aux (i,j+1) (a::acc)
        | (None, Some b) -> aux (i,j+1) (b::acc)
        | (None, None) -> aux (i,j+1) acc
    )
  in aux (0,0) []

let distance final_line (x,y) =
  match final_line with
  | ('x', value) -> abs (x - value)
  | ('y', value) -> abs (y - value)
  | _ -> 0
let in_final_line (x,y) final_line =
  match final_line with
  | ('x', value) -> x = value
  | ('y', value) -> y = value
  | _ -> false
let find_path final_line (x,y) = 
  let rec aux (x,y) acc = 
    if (acc > 100) then 100
    else(
    match (x,y) with
    | (x,y) when (in_final_line (x,y) final_line) -> acc
    | (x,y) -> let lst = list_of_moves (x,y) in
    let rec aux2 lst acc new_pos = match lst with
      | [] -> new_pos
      | (x,y)::q -> let value = distance final_line (x,y) in
        if value < acc then aux2 q value (x,y)
        else aux2 q acc new_pos
    in let (xnew,ynew) = aux2 lst max_int (x,y) in
    aux (xnew,ynew) (acc+1)
    )

  in aux (x,y) 0
let value_of_a_move (x,y) =
  let final_line = color_to_final_pos (current_player ()).color in
  find_path final_line (x,y)
let test_move_with_the_wall (x,y) (x',y') (x1,y1) (x2,y2) = 
  if ((x + x') / 2, (y + y') / 2) = (x1,y1) || ((x + x') / 2, (y + y') / 2) = (x2,y2) then true
  else false

let find_path_with_a_wall final_line (x,y) (x1,y1) (x2,y2) = 
  let rec aux (x,y) acc = 
    if (acc > 100) then 100
    else(
    match (x,y) with
    | (x,y) when (in_final_line (x,y) final_line) -> acc
    | (x,y) -> let lst = (
      let rec move_you_can_do_with_the_wall moves = 
        match moves with
        | [] -> []
        | (x',y')::q -> if (test_move_with_the_wall (x,y) (x',y') (x1,y1) (x2,y2)) then move_you_can_do_with_the_wall q
          else (x',y')::(move_you_can_do_with_the_wall q)
  in move_you_can_do_with_the_wall (list_of_moves (x,y))
     ) in(*
     Format.printf "lst : %d\n" (List.length lst);
     Format.printf "lst : %d\n" (List.length (list_of_moves (x,y)));
     Format.printf "the wall : (%d,%d) (%d,%d)\n" x1 y1 x2 y2;
     Format.printf "pos : (%d,%d)\n" x y;*)

    let rec aux2 lst acc new_pos = match lst with
      | [] -> new_pos
      | (x,y)::q -> let value = distance final_line (x,y) in
     (* Format.printf "value : %d\n" value;
      Format.printf "(x,y) : (%d,%d)\n" x y;*)
        if value < acc then aux2 q value (x,y)
        else aux2 q acc new_pos
    in let (xnew,ynew) = aux2 lst max_int (x,y) in
    aux (xnew,ynew) (acc+1)
    )
  in aux (x,y) 0

let value_of_the_ennemy_move () =
  let have_list_of_player = have_all_player_in_board () in
  Random.self_init();
  let choose_a_color = Random.int (List.length have_list_of_player) in
  let color =( match choose_a_color with
  | 0 -> Red
  | 1 -> Blue 
  | 2 -> Green
  | 3 -> Yellow 
  | _ -> Blue
  )
in let color = ( match color with
  | color when (color = (current_player ()).color) -> (
  match color with
  | Red -> Blue
  | Blue -> Red
  | Green -> Yellow
  | Yellow -> Green
)
| _ -> color)
  in
  let final_line = color_to_final_pos color in
  let find_the_pos_of_the_color = List.find (fun (x,y) -> (match get_color_of_a_position (x,y) with | Some p -> p | None -> current_player()).color = color) in
  let (x,y) = find_the_pos_of_the_color have_list_of_player in
  (*Format.printf "color : %s" (match color with | Red -> "Red" | Blue -> "Blue" | Green -> "Green" | Yellow -> "Yellow");*)
  find_path final_line (x,y)

let value_of_the_ennemy_move_with_the_wall (x1,y1) (x2,y2) =
  let have_list_of_player = have_all_player_in_board () in
  Random.self_init();
  let choose_a_color = Random.int (List.length have_list_of_player) in
  let color =( match choose_a_color with
  | 0 -> Red
  | 1 -> Blue 
  | 2 -> Green
  | 3 -> Yellow 
  | _ -> Blue
  )
in let color = ( match color with
  | color when (color = (current_player ()).color) -> (
  match color with
  | Red -> Blue
  | Blue -> Red
  | Green -> Yellow
  | Yellow -> Green
)
| _ -> color)
  in
  let final_line = color_to_final_pos color in
  let find_the_pos_of_the_color = List.find (fun (x,y) -> (match get_color_of_a_position (x,y) with | Some p -> p | None -> current_player()).color = color) in
  let (x,y) = find_the_pos_of_the_color have_list_of_player in
  (*Format.printf "color : %s" (match color with | Red -> "Red" | Blue -> "Blue" | Green -> "Green" | Yellow -> "Yellow");*)
  find_path_with_a_wall final_line (x,y) (x1,y1) (x2,y2)

  
let test_move (*nb_player*) pos =
  (*Format.printf "test_move\n";
  Format.printf "Player of color :\n";
  (
  match (current_player ()).color with
  | Red -> Format.printf "Red\n"
  | Blue -> Format.printf "Blue\n"
  | Green -> Format.printf "Green\n"
  | Yellow -> Format.printf "Yellow\n"
  );

  Format.printf "nb_player : %d\n" nb_player;
  Format.printf "pos : (%d,%d)\n" (fst pos) (snd pos);*)

  let lstMv = list_of_moves pos in 
  match List.find_opt  (fun (x,y) -> in_final_line (x,y) (color_to_final_pos (current_player ()).color)) lstMv with
  | Some (x,y) -> Moving (x,y)
  | None -> (
  let lstWall = list_of_wall () in
  let rec aux test_all_moves acc value_of_acc = match test_all_moves with
    | [] -> acc,value_of_acc
    | (x,y)::q ->let value_of_move = value_of_a_move (x,y) in
      if value_of_move < value_of_acc then aux q (x,y) value_of_move
      else aux q acc value_of_acc
  in let (x,y),interest_of_the_move = aux lstMv pos max_int in
  if (current_player()).walls_left = 0 then Moving (x,y)
  else
  (*Format.printf "interest_of_the_move : %d\n" interest_of_the_move;*)
  (*Format.printf "lstWall : %d\n" (List.length lstWall);*)

  (*Format.printf "pos : (%d,%d)\n" x y; *)
  let rec aux2 test_all_wall acc value_of_acc = match test_all_wall with
    | [] -> acc,value_of_acc
    | ((x1,y1),(x2,y2))::q -> let value_of_wall = (value_of_the_ennemy_move_with_the_wall (x1,y1) (x2,y2) ) - (value_of_the_ennemy_move ())  in 
      if value_of_wall > value_of_acc then aux2 q ((x1,y1),(x2,y2)) value_of_wall
      else aux2 q acc value_of_acc
  in let ((x1,y1),(x2,y2)),interest_of_the_wall = aux2 lstWall ((-1,-1),(-1,-1)) 0 in
  if interest_of_the_wall = 0 then Moving (x,y)
  else(
  (*Format.printf "pos : (%d,%d) (%d,%d)\n" x1 y1 x2 y2;
  Format.printf "interest_of_the_move : %d\n" interest_of_the_move;
  Format.printf "interest_of_the_wall : %d\n" interest_of_the_wall;*)
  (*Format.printf "Player : %s\n" (match (current_player ()).color with | Red -> "Red" | Blue -> "Blue" | Green -> "Green" | Yellow -> "Yellow");
  Format.printf "pos : (%d,%d)\n" (fst pos) (snd pos);
  Format.printf "interest_of_the_move : %d\n"  ((distance (color_to_final_pos (current_player ()).color) pos ) / 2  -  interest_of_the_move);
  Format.printf "interest_of_the_wall : %d\n" interest_of_the_wall;*)
  if ((distance (color_to_final_pos (current_player ()).color) pos )/2 -  interest_of_the_move) > interest_of_the_wall then Moving (x,y)
  else Placing_wall ((x1,y1),(x2,y2))
  ))




(** This function defines our strategy for my player*)
let better_move2 pos =
  test_move pos