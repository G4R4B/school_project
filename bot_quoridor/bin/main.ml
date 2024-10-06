open Quoridor.Engine
open Quoridor.Types
open Quoridor.Board
open Betterbot

let run_game_with_string player_lst =
  Random.self_init ();
  let rec aux () =
    print_board ();
    try
      let winner = winning_player () in
      winner
    with NoWinningPlayer _ ->
      play ();
      aux ()
  in
  add_players player_lst;
  start_game ();
  aux ()
let create_lst_of_player nb_players walls_left =
  let colors = [ Red; Blue; Green; Yellow ] in
  let positions =
    [
      (board_size / 2, 0);
      (board_size / 2, board_size - 1);
      (0, board_size / 2);
      (board_size - 1, board_size / 2);
    ]
  in
  if nb_players <> 2 && nb_players <> 4 then
    raise
      (InvalidNumberPlayer
         (nb_players, "Number of players must be 2 or 4 to start the game"))
  else
    List.init nb_players (fun i ->
        create_player (List.nth positions i) walls_left (List.nth colors i)
        (if i = 0 then better_move 
        else if i = 1 then better_move
        else if i = 2 then better_move
        else better_move))

        


let () =
  let rec count_number_of_win_of_my_bot lst_player acc acc_bot1 acc_bot2 acc_bot_3 acc_bot4 =
    Format.printf ("acc : %d acc_bot1 : %d acc_bot_2 : %d acc_bot3 : %d acc_bot4 : %d") acc acc_bot1 acc_bot2 acc_bot_3 acc_bot4;
    if acc = 100 then (acc_bot1, acc_bot2 , acc_bot_3, acc_bot4)
    else
    match (run_game_with_string lst_player).color with
    | Red -> count_number_of_win_of_my_bot lst_player (acc+1) (acc_bot1+1) (acc_bot2) (acc_bot_3) (acc_bot4)
    | Blue -> count_number_of_win_of_my_bot lst_player (acc+1) (acc_bot1) (acc_bot2+1) (acc_bot_3) (acc_bot4)
    | Green -> count_number_of_win_of_my_bot lst_player (acc+1) (acc_bot1) (acc_bot2) (acc_bot_3+1) (acc_bot4)
    | Yellow -> count_number_of_win_of_my_bot lst_player (acc+1) acc_bot1 (acc_bot2) (acc_bot_3) (acc_bot4+1)
  in
  let (a,b, c ,d) = (count_number_of_win_of_my_bot (create_lst_of_player 4 5) 0 0 0 0 0) in 
  Format.printf "\n\n %d %d %d %d %!" a b c d;
