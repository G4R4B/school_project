open Quoridor.Board
open Quoridor.Types


(**This function returns a movement with a position where the player moves based on their current position
    @param pos the player's initial position
    @raise NoMovePossible when the player has no possible movement
    @return the position where the player must move  *)
    let random_move pos =
      let lstMv = list_of_moves pos in
      match lstMv with
      | [] -> raise (NoMovePossible "There is no movement possible for this player")
      | _ ->
          let r = Random.int (List.length lstMv) in
          let newPos = List.nth lstMv r in
          Moving newPos
    
    (**This function returns 2 random positions where we will and we can place a wall*)
    let pos_wall_random () =
      let rec generate_random_wall_pos () =
        let x1 = Random.int board_size in
        let y1 = Random.int board_size in
        let r = Random.int 4 in
        let xv, yv = List.nth move_vectors r in
        try
          validate_wall_placement (current_player ()) (x1, y1) (x1 + xv, y1 + yv);
          ((x1, y1), (x1 + xv, y1 + yv))
        with
        | InvalidWallPosition _ -> generate_random_wall_pos ()
        | InvalidPosition _ -> generate_random_wall_pos ()
        | InvalidWallPlacement _ -> generate_random_wall_pos ()
      in
      let wall_pos1, wall_pos2 = generate_random_wall_pos () in
      Placing_wall (wall_pos1, wall_pos2)
    
    (** This function defines our strategy for our players which is to play randomly*)
    let det_move pos =
      let r = Random.int 3 in
      if r == 0 && (current_player ()).walls_left > 0 then pos_wall_random ()
      else random_move pos
    
    (** Creates and returns the list of players with their position, color and our strategy 
        @param nb_players The number of players to add to the game
        @raise InvalidNumberPlayer if the number of players is not 2 or 4.
        @return the list of players to add to the game
        *)
