import machine
import time
from TM1638Driver import TM1638
from mancala import Board


def get_pocket_from_player(player):
    while True:
        key = player_board[player].read_keys()

        if key & TM1638.KEY_1 == TM1638.KEY_1:
            return 0
        if key & TM1638.KEY_2 == TM1638.KEY_2:
            return 1
        if key & TM1638.KEY_3 == TM1638.KEY_3:
            return 2
        if key & TM1638.KEY_4 == TM1638.KEY_4:
            return 3
        if key & TM1638.KEY_5 == TM1638.KEY_5:
            return 4
        if key & TM1638.KEY_6 == TM1638.KEY_6:
            return 5

        time.sleep_ms(10)


def display_player(player):
    board_side = game.get_side(player)

    display_str = ""
    for i in range(6):
        display_str += "{0:1d}".format(board_side.pockets[i] % 10)
        if board_side.pockets[i] >= 10:
            display_str += "."
    display_str += "{0:2d}".format(board_side.store)

    player_board[player].write_string(display_str)


if __name__ == '__main__':
    print('Lets play Mancala')

    player_board = [TM1638(machine.Pin(5, machine.Pin.OUT),
                           machine.Pin(7, machine.Pin.OUT),
                           machine.Pin(8, machine.Pin.OUT), 2),
                    TM1638(machine.Pin(6, machine.Pin.OUT),
                           machine.Pin(7, machine.Pin.OUT),
                           machine.Pin(8, machine.Pin.OUT), 2)]

    player_board[0].write_string("Mancala")
    player_board[1].write_string("Game 1.1")

    time.sleep_ms(5000)

    game = Board()
    display_player(0)
    display_player(1)

    current_player = 0
    other_player = 1
    while True:

        # Your turn
        player_board[current_player].write_string("YourTurn")
        for i in range(6):
            if game.get_side(current_player).pockets[i] > 0:
                player_board[current_player].toggle_led(i, True)
            else:
                player_board[current_player].toggle_led(i, False)
            player_board[other_player].toggle_led(i, False)

        time.sleep_ms(2000)
        display_player(current_player)

        selected_pocket = get_pocket_from_player(current_player)

        game_status = game.make_move(current_player, selected_pocket)
        display_player(0)
        display_player(1)

        if game_status == Board.STATUS_IN_PROGRESS:
            current_player = 1 if current_player == 0 else 0
            other_player = 1 if other_player == 0 else 0
        elif game_status == Board.STATUS_PLAYER_ONE_WINS:
            player_board[0].write_string("You won!")
            player_board[1].write_string("You Lose")
            time.sleep_ms(4000)
            break
        elif game_status == Board.STATUS_PLAYER_TWO_WINS:
            player_board[0].write_string("You Lose")
            player_board[1].write_string("You won!")
            time.sleep_ms(4000)
            break
        elif game_status == Board.STATUS_DRAW:
            player_board[0].write_string("Draw!")
            player_board[1].write_string("Draw!")
            time.sleep_ms(2000)
            break
        elif game_status == Board.STATUS_INVALID_MOVE_NO_STONES:
            player_board[current_player].write_string("Bad Move")
            time.sleep_ms(3000)
            display_player(current_player)

    display_player(0)
    display_player(1)
    time.sleep_ms(5000)
    player_board[0].write_string("GameOver")
    player_board[1].write_string("GameOver")
