from abc import ABC, abstractmethod
from enum import Enum


class Color(Enum):
    White = 1
    Black = 2

    def __neg__(self):
        return Color.White if self == Color.Black else Color.Black


class Piece(ABC):
    color = None
    current_position_x = None
    current_position_y = None

    def place_on_board(self, board):
        board[self.current_position_x][self.current_position_y] = self

    def __init__(self, color: Color, current_position_x, current_position_y, board):
        self.color = color
        self.current_position_x = current_position_x
        self.current_position_y = current_position_y
        board[self.current_position_x][self.current_position_y] = self

    def move(self, new_position_x, new_position_y, board):
        board[self.current_position_x][self.current_position_y] = None
        self.current_position_x = new_position_x
        self.current_position_y = new_position_y
        board[new_position_x][new_position_y] = self

    @abstractmethod
    def can_move(self, new_position_x, new_position_y, board):
        pass

    def can_capture(self, new_position_x, new_position_y, board):
        return self.can_move(new_position_x, new_position_y, board)

    def try_to_move(self, new_position_x, new_position_y, board):
        if board[new_position_x][new_position_y] is not None and board[new_position_x][new_position_y].color == self.color:
            return False
        x, y = self.current_position_x, self.current_position_y
        self.move(new_position_x, new_position_y, board)
        if not self.can_move(x, y, board):
            self.move(x, y, board)
            return False
        return True


class Pawn(Piece, ABC):

    def is_path_clear(self, new_position_x, new_position_y, board):
        if self.color == Color.White:
            for i in range(self.current_position_y - 1, new_position_y, -1):
                if board[new_position_x][i] is not None:
                    return False
            return True
        for i in range(self.current_position_y + 1, new_position_y):
            if board[new_position_x][i] is not None:
                return False
        return True

    def can_move(self, new_position_x, new_position_y, board):
        if self.color == Color.White:
            if new_position_x == self.current_position_x and self.is_path_clear(new_position_x, new_position_y, board) and \
               (new_position_y == self.current_position_y - 1 or (new_position_y == self.current_position_y - 2 and self.current_position_y == 6)):
                return True
            return False
        else:
            if new_position_x == self.current_position_x and self.is_path_clear(new_position_x, new_position_y, board) and \
               (new_position_y == self.current_position_y + 1 or (new_position_y == self.current_position_y + 2 and self.current_position_y == 1)):
                return True
            return False

    def can_capture(self, new_position_x, new_position_y, board):
        if self.color == Color.White and new_position_y == self.current_position_y - 1 and \
           (new_position_x == self.current_position_x + 1 or new_position_x == self.current_position_x - 1) and \
           board[new_position_x][new_position_y] is not None and board[new_position_x][new_position_y].color != self.color:
            return True
        elif self.color == Color.Black and new_position_y == self.current_position_y + 1 and \
            (new_position_x == self.current_position_x + 1 or new_position_x == self.current_position_x - 1) and \
                board[new_position_x][new_position_y] is not None and board[new_position_x][new_position_y].color != self.color:
            return True

    def try_to_move(self, new_position_x, new_position_y, board):
        if board[new_position_x][new_position_y] is not None and board[new_position_x][new_position_y].color == self.color:
            return False
        if self.can_move(new_position_x, new_position_y, board):
            self.move(new_position_x, new_position_y, board)
            return True
        return False


class Bishop(Piece, ABC):

    def bishop_is_path_clear(self, new_position_x, new_position_y, board):
        temp_y = self.current_position_y
        if self.current_position_y > new_position_y:
            if self.current_position_x > new_position_x:
                for i in range(self.current_position_x - 1, new_position_x, -1):
                    if board[i][temp_y - 1] is not None:
                        return False
                    temp_y -= 1
            else:
                for i in range(self.current_position_x + 1, new_position_x):
                    if board[i][temp_y - 1] is not None:
                        return False
                    temp_y -= 1
        else:
            if self.current_position_x > new_position_x:
                for i in range(self.current_position_x - 1, new_position_x, -1):
                    if board[i][temp_y + 1] is not None:
                        return False
                    temp_y += 1
            else:
                for i in range(self.current_position_x + 1, new_position_x):
                    if board[i][temp_y + 1] is not None:
                        return False
                    temp_y += 1
        return True

    def can_move(self, new_position_x, new_position_y, board):
        for i in range(1, 8):
            if (new_position_x == self.current_position_x + i or new_position_x == self.current_position_x - i) and \
               (new_position_y == self.current_position_y + i or new_position_y == self.current_position_y - i) and \
               self.bishop_is_path_clear(new_position_x, new_position_y, board):
                return True
        return False


class Rook(Piece, ABC):

    can_castle = True

    def rook_is_path_clear(self, new_position_x, new_position_y, board):
        if self.current_position_y > new_position_y:
            for i in range(self.current_position_y - 1, new_position_y, -1):
                if board[new_position_x][i] is not None:
                    return False
        elif self.current_position_y < new_position_y:
            for i in range(self.current_position_y + 1, new_position_y):
                if board[new_position_x][i] is not None:
                    return False
        else:
            if self.current_position_x > new_position_x:
                for i in range(self.current_position_x - 1, new_position_x, -1):
                    if board[i][new_position_y] is not None:
                        return False
            else:
                for i in range(self.current_position_x + 1, new_position_x):
                    if board[i][new_position_y] is not None:
                        return False
        return True

    def can_move(self, new_position_x, new_position_y, board):
        for i in range(1, 8):
            if (new_position_x == self.current_position_x and new_position_y == self.current_position_y - i) or \
               (new_position_y == self.current_position_y and new_position_x == self.current_position_x - i) or \
               (new_position_x == self.current_position_x and new_position_y == self.current_position_y + i) or \
               (new_position_y == self.current_position_y and new_position_x == self.current_position_x + i):
                if self.rook_is_path_clear(new_position_x, new_position_y, board):
                    return True
        return False


class King(Piece, ABC):

    can_castle = True
    possible_moves = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    def can_move(self, new_position_x, new_position_y, board):
        if board[new_position_x][new_position_y] is not None and board[new_position_x][new_position_y].color == self.color:
            return False
        for x, y in self.possible_moves:
            if new_position_x == self.current_position_x + x and new_position_y == self.current_position_y + y:
                return True
        return False


class Queen(Bishop, Rook, ABC):

    def queen_is_path_clear(self, new_position_x, new_position_y, board):
        if self.current_position_x != new_position_x and self.current_position_y != new_position_y:
            return self.bishop_is_path_clear(new_position_x, new_position_y, board)
        return self.rook_is_path_clear(new_position_x, new_position_y, board)

    def can_move(self, new_position_x, new_position_y, board):
        for i in range(1, 8):
            if (new_position_x == self.current_position_x + i or new_position_x == self.current_position_x - i) and \
               (new_position_y == self.current_position_y + i or new_position_y == self.current_position_y - i) or \
               (new_position_x == self.current_position_x and new_position_y == self.current_position_y - i) or \
               (new_position_y == self.current_position_y and new_position_x == self.current_position_x - i) or \
               (new_position_x == self.current_position_x and new_position_y == self.current_position_y + i) or \
               (new_position_y == self.current_position_y and new_position_x == self.current_position_x + i):
                if self.queen_is_path_clear(new_position_x, new_position_y, board):
                    return True
        return False


class Knight(Piece, ABC):

    possible_moves = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (-1, 2), (1, -2), (-1, -2)]

    def can_move(self, new_position_x, new_position_y, board):
        for x, y in self.possible_moves:
            if new_position_x == self.current_position_x + x and new_position_y == self.current_position_y + y:
                return True
        return False

