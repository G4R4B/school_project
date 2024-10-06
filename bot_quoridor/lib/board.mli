type cell_content
(** Represents the content of a cell on the game board. Can be empty, a wall, or a player. *)

type board
(** Represents the game board as a matrix of cell contents. *)

type state
(** Represents the current state of the game, including the list of players and the game status. *)

val board_size : int
(** The size of the game board. *)

val move_vectors : (int * int) list
(** The list of possible move directions for a player. *)

val start_game : unit -> unit
(** Starts the game.
    @raise InvalidNumberPlayer if the number of players is neither two nor four.
    @raise InvalidGameState if the game is not in the WaitingToStart state. *)

val current_player : unit -> Types.player
(** Returns the current player.
    @raise NoPlayersInGame if there are no players in the game. *)

val validate_position : Types.position -> unit
(** Validates a position on the game board.
    @param pos The position to validate.
    @raise InvalidPosition if the position is outside the board boundaries. *)

val is_wall_position : Types.position -> bool
(** Determines if a position is a valid wall position.
    @param pos The position to check.
    @return true if it is a wall position, false otherwise. *)

val is_player_position : Types.position -> bool
(** Determines if a position is a valid player position.
    @param pos The position to check.
    @return true if it is a player position, false otherwise. *)

val is_wall : Types.position -> bool
(** Checks if there is a wall at the given position.
    @param pos The position to check.
    @return true if there is a wall, false otherwise. *)

val is_player : Types.position -> bool
(** Checks if there is a player at the given position.
    @param pos The position to check.
    @return true if there is a player, false otherwise. *)

val is_wall_between : Types.position -> Types.position -> bool
(** Checks if there is a wall between two positions.
    @param pos1 The first position.
    @param pos2 The second position.
    @return true if there is a wall between the positions, false otherwise.
    @raise InvalidPositionPair if the positions are the same, not adjacent, or not player positions. *)

val adjacent_walls : Types.position -> (int * int) list
(** Returns a list of positions of walls adjacent to a given player position.
    @param pos The player's position.
    @raise InvalidPlayerPosition if the given position is not a player's position.
    @return A list of positions where walls are present adjacent to the given player position. *)

val adjacent_players : Types.position -> (int * int) list
(** Returns a list of positions of players adjacent to a given player position.
    @param pos The player's position.
    @raise InvalidPlayerPosition if the given position is not a player's position.
    @return A list of positions where players are present adjacent to the given player position. *)

val list_of_moves : Types.position -> Types.position list
(** Provides a list of all possible moves from a given position.
    @param pos The current position of the player.
    @return A list of positions representing all valid moves from the given position.
    @raise InvalidPlayerPosition if the given position is not a player's position. 
    @note This function takes into account the presence of walls and other players. *)

val validate_wall_placement :
  Types.player -> Types.position -> Types.position -> unit
(** Validates the placement of a wall by a player.
    @param player The player placing the wall.
    @param pos1 The first position of the wall.
    @param pos2 The second position of the wall.
    @raise InvalidWallPlacement if the player has no walls left or the wall placement is invalid.
    @raise InvalidWallPosition if the wall positions are not valid or not adjacent and aligned.
    @raise InvalidGameState if the game is not in progress. *)

val add_all_players_to_board : Types.player list -> unit

val play : unit -> unit
(** Makes a player play thanks to his strategy (places a wall or moves the player).*)

val winning_player : unit -> Types.player
(** Returns the player who has reached their target zone.
    @raise NoWinningPlayer if no player has reached their target zone. *)

val print_board : unit -> unit
(** Prints the current state of the game board. *)

val color_to_string : Types.player -> string
(** Returns the color of a player as a string. *)

val get_color_of_a_position : Types.position -> Types.player option
(** Returns the color of a player at a given position.
    @param pos The position to check.
    @return The color of the player at the given position.
    @raise InvalidPlayerPosition if the given position is not a player's position. *)
