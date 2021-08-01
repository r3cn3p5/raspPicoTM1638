class BoardSide:

    def __init__(self):
        self._store = 0
        self._pockets = []
        for x in range(0, 6):
            self.pockets.append(4)

    @property
    def store(self):
        return self._store

    @store.setter
    def store(self, store):
        self._store = store

    @property
    def pockets(self):
        return self._pockets


class Board:
    STATUS_IN_PROGRESS = 0
    STATUS_PLAYER_ONE_WINS = 1
    STATUS_PLAYER_TWO_WINS = 2
    STATUS_DRAW = 3
    STATUS_PLAYER_REPLAY = 4
    STATUS_INVALID_MOVE_NO_STONES = 5

    def __init__(self):

        self._sides = []
        for s in range(0, 2):
            self._sides.append(BoardSide())

    def make_move(self, player, pocket):

        if self._sides[player].pockets[pocket] == 0:
            return Board.STATUS_INVALID_MOVE_NO_STONES

        status = Board.STATUS_IN_PROGRESS
        side = player

        stones = self._sides[side].pockets[pocket]
        self._sides[side].pockets[pocket] = 0
        pocket += 1

        while stones > 0:
            if pocket >= 6:
                if side == player:
                    self._sides[side].store += 1
                    status = Board.STATUS_PLAYER_REPLAY if stones == 1 else status
                    stones -= 1

                pocket = 0

                side = 1 if side == 0 else 0
                continue

            opposite_side = 1 if side == 0 else 0
            if side == player \
                    and stones == 1 \
                    and self._sides[side].pockets[pocket] == 0 \
                    and self._sides[opposite_side].pockets[5 - pocket] > 0:
                self._sides[side].store += 1
                self._sides[side].pockets[pocket] = 0
                self._sides[side].store += self._sides[opposite_side].pockets[5 - pocket]
                self._sides[opposite_side].pockets[5 - pocket] = 0
                break

            self._sides[side].pockets[pocket] += 1
            stones -= 1
            pocket += 1

        # if one player has empty side then the other takes all there remaining stones.
        for s in range(0, 2):
            os = 1 if s == 0 else 0

            t = 0
            for p in range(0, 6):
                t += self._sides[s].pockets[p]

            if t == 0:
                for p in range(0, 6):
                    t += self._sides[os].pockets[p]
                    self._sides[os].pockets[p] = 0

                self._sides[os].store += t

                if self._sides[0].store > self._sides[1].store:
                    status = Board.STATUS_PLAYER_ONE_WINS
                elif self._sides[0].store < self._sides[1].store:
                    status = Board.STATUS_PLAYER_TWO_WINS
                else:
                    status = Board.STATUS_DRAW
                break

        return status

    def get_side(self, player):
        return self._sides[player]

    def __str__(self):

        ret_str = "S({0:2d}) ".format(self._sides[0].store)
        for p in range(5, -1, -1):
            ret_str += "{0:1d}({1:2d}) ".format(p + 1, self._sides[0].pockets[p])
        ret_str += "\n      "
        for p in range(0, 6):
            ret_str += "{0:1d}({1:2d}) ".format(p + 1, self._sides[1].pockets[p])
        ret_str += "S({0:2d})".format(self._sides[1].store)

        return ret_str
