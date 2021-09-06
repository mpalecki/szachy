from Pieces import *
from Images import *

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
TILESIZE = 70
list_of_pieces = []
current_turn = Color.White


def place_pieces(board):

    piece_type = {
        0: Rook,
        1: Knight,
        2: Bishop,
        3: King,
        4: Queen,
        5: Bishop,
        6: Knight,
        7: Rook
    }

    for k in piece_type.keys():
        new_white_piece = piece_type[k](Color.White, k, 7, board)
        new_black_piece = piece_type[k](Color.Black, k, 0, board)
        list_of_pieces.append(new_white_piece)
        list_of_pieces.append(new_black_piece)

    for i in range(8):
        new_white_pawn = Pawn(Color.White, i, 6, board)
        new_black_pawn = Pawn(Color.Black, i, 1, board)
        list_of_pieces.append(new_white_pawn)
        list_of_pieces.append(new_black_pawn)


def promotion_choice_surface(pawn):
    surface = pygame.Surface((TILESIZE, TILESIZE * 4))
    surface.fill("red")
    if pawn.color == Color.White:
        surface.blit(white_queen_image, (0, 0))
        surface.blit(white_knight_image, (0, TILESIZE))
        surface.blit(white_rook_image, (0, TILESIZE * 2))
        surface.blit(white_bishop_image, (0, TILESIZE * 3))
    else:
        surface.blit(black_queen_image, (0, 0))
        surface.blit(black_knight_image, (0, TILESIZE))
        surface.blit(black_rook_image, (0, TILESIZE * 2))
        surface.blit(black_bishop_image, (0, TILESIZE * 3))

    return surface


def find_pawn_to_promote(board):
    for x in range(8):
        if type(board[x][0]) == Pawn:
            return board[x][0]
        elif type(board[x][7]) == Pawn:
            return board[x][7]


def check_promotion(board_surface, board):
    pawn = find_pawn_to_promote(board)
    if pawn is not None:
        surface = promotion_choice_surface(pawn)
        if pawn.color == Color.White:
            board_surface.blit(surface, (pawn.current_position_x * TILESIZE, 0))
        else:
            board_surface.blit(surface, (pawn.current_position_x * TILESIZE, 280))


def click_on_promotion_surface(pawn, board):

    pawn_dict = {
        0: Queen,
        1: Knight,
        2: Rook,
        3: Bishop
    }

    pos = pygame.mouse.get_pos()
    x = (pos[0] - 360) // TILESIZE
    y = (pos[1] - 80) // TILESIZE
    pawn_x, pawn_y = pawn.current_position_x, pawn.current_position_y
    if pawn.color == Color.White:
        if x == pawn.current_position_x and 0 <= y <= 3:
            list_of_pieces.remove(pawn)
            for k in pawn_dict.keys():
                if y == k:
                    new_piece = pawn_dict[k](Color.White, pawn_x, pawn_y, board)
                    list_of_pieces.append(new_piece)
    else:
        if x == pawn.current_position_x and 4 <= y <= 7:
            list_of_pieces.remove(pawn)
            for k in pawn_dict.keys():
                if y - 4 == k:
                    new_piece = pawn_dict[k](Color.Black, pawn_x, pawn_y, board)
                    list_of_pieces.append(new_piece)


def create_board_surf():
    board_surf = pygame.Surface((TILESIZE * 8, TILESIZE * 8))
    gray = False
    for y in range(8):
        for x in range(8):
            rect = pygame.Rect(x * TILESIZE, y * TILESIZE, TILESIZE, TILESIZE)
            pygame.draw.rect(board_surf, pygame.Color('gray' if gray else 'white'), rect)
            gray = not gray
        gray = not gray
    return board_surf


def create_board():
    board = [[None for i in range(8)] for j in range(8)]
    return board


def find_king(turn):
    for obj in list_of_pieces:
        if type(obj) == King and obj.color == turn:
            return obj


def is_check(pos_x, pos_y, board, checkers):
    for obj in list_of_pieces:
        if obj.color != current_turn and obj.can_capture(pos_x, pos_y, board):
            checkers.append(obj)
            return True
    return False


def find_fields_between(x1, y1, x2, y2):
    fields_between = []
    if abs(x1 - x2) == abs(y1 - y2):
        counter = 0
        for i in range(min(x1, x2) + 1, max(x1, x2)):
            if x1 > x2 and y1 < y2:
                fields_between.append((i, max(y1, y2) - counter - 1))
                counter += 1
            elif x1 > x2 and y1 > y2:
                fields_between.append((i, min(y1, y2) + counter + 1))
                counter += 1
            elif x1 < x2 and y1 < y2:
                fields_between.append((i, min(y1, y2) + counter + 1))
                counter += 1
            elif x1 < x2 and y1 > y2:
                fields_between.append((i, max(y1, y2) - counter - 1))
                counter += 1
    elif x1 == x2:
        if y1 > y2:
            for i in range(y2, y1 - 1):
                fields_between.append((x1, i + 1))
        elif y1 < y2:
            for i in range(y1 + 1, y2):
                fields_between.append((x1, i))
    elif y1 == y2:
        if x1 > x2:
            for i in range(x1 - 1, x2, -1):
                fields_between.append((i, y1))
        elif x1 < x2:
            for i in range(x1 + 1, x2):
                fields_between.append((i, y1))
    return fields_between


def is_checkmate(king, board, checkers):
    fields_between = []

    for checker in checkers:
        fields_between.append((checker.current_position_x, checker.current_position_y))
        fields_between += find_fields_between(checker.current_position_x, checker.current_position_y,
                                              king.current_position_x, king.current_position_y)
    if len(checkers) == 1:
        for obj in list_of_pieces:
            if obj.color == current_turn and type(obj) != King:
                for x, y in fields_between:
                    if obj.can_move(x, y, board) or obj.can_capture(x, y, board):
                        return False
    for x, y in king.possible_moves:
        if 0 <= king.current_position_x + x <= 7 and 0 <= king.current_position_y + y <= 7:
            if king.can_move(king.current_position_x + x, king.current_position_y + y, board):
                board[king.current_position_x][king.current_position_y] = None
                if not is_check(king.current_position_x + x, king.current_position_y + y, board, checkers):
                    board[king.current_position_x][king.current_position_y] = king
                    return False
                board[king.current_position_x][king.current_position_y] = king
    return is_check(king.current_position_x, king.current_position_y, board, checkers)


def castling(x, y, obj, board):
    global current_turn
    checkers = []
    if current_turn == Color.White:
        if x == 1 and y == 7:
            fields = find_fields_between(0, 7, 3, 7)
            for field_x, field_y in fields:
                if board[field_x][field_y] is None and not is_check(field_x, field_y, board, checkers) and obj.can_castle and board[0][7].can_castle:
                    continue
                else:
                    return
            obj.move(1, 7, board)
            board[0][7].move(2, 7, board)
            current_turn = -current_turn
        elif x == 5 and y == 7:
            fields = find_fields_between(3, 7, 7, 7)
            for field_x, field_y in fields:
                if board[field_x][field_y] is None and not is_check(field_x, field_y, board, checkers) and obj.can_castle and board[7][7].can_castle:
                    continue
                else:
                    return
            obj.move(5, 7, board)
            board[7][7].move(4, 7, board)
            current_turn = -current_turn
    else:
        if x == 1 and y == 0:
            fields = find_fields_between(0, 0, 3, 0)
            for field_x, field_y in fields:
                if board[field_x][field_y] is None and not is_check(field_x, field_y, board, checkers) and obj.can_castle and board[0][0].can_castle:
                    continue
                else:
                    return
            obj.move(1, 0, board)
            board[0][0].move(2, 0, board)
            current_turn = -current_turn
        elif x == 5 and y == 0:
            fields = find_fields_between(3, 0, 7, 0)
            for field_x, field_y in fields:
                if board[field_x][field_y] is None and not is_check(field_x, field_y, board, checkers) and obj.can_castle and board[7][0].can_castle:
                    continue
                else:
                    return
            obj.move(5, 0, board)
            board[7][0].move(4, 0, board)
            current_turn = -current_turn


def click_on_board(board):
    pos = pygame.mouse.get_pos()
    x = (pos[0] - 360) // TILESIZE
    y = (pos[1] - 80) // TILESIZE
    if 360 <= pos[0] <= 920 and 80 <= pos[1] <= 640 and board[x][y] is not None and board[x][y].color == current_turn:
        return board[x][y]


def move_piece(board, temp1):
    global current_turn
    pos = pygame.mouse.get_pos()
    checkers = []
    x = (pos[0] - 360) // TILESIZE
    y = (pos[1] - 80) // TILESIZE
    if 360 <= pos[0] <= 920 and 80 <= pos[1] <= 640:
        for obj in list_of_pieces:
            if obj == temp1:
                king = find_king(current_turn)
                if is_check(king.current_position_x, king.current_position_y, board, checkers):
                    old_x, old_y, capture = obj.current_position_x, obj.current_position_y, None
                    if board[x][y] is not None and board[x][y].color != obj.color:
                        if obj.can_capture(x, y, board):
                            capture = board[x][y]
                    if board[x][y] in checkers and capture is not None:
                        list_of_pieces.remove(capture)
                        if type(obj) == Pawn:
                            obj.move(x, y, board)
                    obj.try_to_move(x, y, board)
                    if is_check(king.current_position_x, king.current_position_y, board, checkers):
                        obj.move(old_x, old_y, board)
                        break
                    else:
                        if capture is not None and capture in list_of_pieces:
                            list_of_pieces.remove(capture)
                    current_turn = -current_turn
                    if type(obj) == Rook or type(obj) == King:
                        obj.can_castle = False
                    break
                elif type(obj) == King:
                    if x == obj.current_position_x and y == obj.current_position_y:
                        break
                    castling(x, y, obj, board)
                    old_x, old_y, capture = obj.current_position_x, obj.current_position_y, None
                    if board[x][y] is not None and board[x][y].color != obj.color:
                        if obj.can_capture(x, y, board):
                            capture = board[x][y]
                    if obj.try_to_move(x, y, board):
                        if is_check(x, y, board, checkers):
                            obj.move(old_x, old_y, board)
                            break
                        current_turn = -current_turn
                    else:
                        break
                    if capture is not None:
                        list_of_pieces.remove(capture)
                    obj.can_castle = False
                    break
                old_x, old_y = obj.current_position_x, obj.current_position_y
                if board[x][y] is None:
                    if obj.try_to_move(x, y, board):
                        if is_check(king.current_position_x, king.current_position_y, board, checkers):
                            obj.move(old_x, old_y, board)
                        else:
                            if type(obj) == Rook:
                                obj.can_castle = False
                            current_turn = -current_turn
                elif board[x][y].color != obj.color:
                    board[old_x][old_y] = None
                    if is_check(king.current_position_x, king.current_position_y, board, checkers):
                        board[old_x][old_y] = obj
                        break
                    board[old_x][old_y] = obj
                    if obj.can_capture(x, y, board):
                        list_of_pieces.remove(board[x][y])
                        if type(obj) == Pawn:
                            obj.move(x, y, board)
                        obj.try_to_move(x, y, board)
                        if type(obj) == Rook:
                            obj.can_castle = False
                        current_turn = -current_turn

    king = find_king(current_turn)
    if is_check(king.current_position_x, king.current_position_y, board, checkers):
        print("szach")
    if is_checkmate(king, board, checkers):
        print("szach-mat")
        current_turn = None


def draw_piece(board_surf, letter, number, piece):
    if type(piece) == Pawn:
        if piece.color == Color.White:
            board_surf.blit(white_pawn_image, (letter * TILESIZE, number * TILESIZE))
        else:
            board_surf.blit(black_pawn_image, (letter * TILESIZE, number * TILESIZE))
    elif type(piece) == Bishop:
        if piece.color == Color.White:
            board_surf.blit(white_bishop_image, (letter * TILESIZE, number * TILESIZE))
        else:
            board_surf.blit(black_bishop_image, (letter * TILESIZE, number * TILESIZE))
    elif type(piece) == Rook:
        if piece.color == Color.White:
            board_surf.blit(white_rook_image, (letter * TILESIZE, number * TILESIZE))
        else:
            board_surf.blit(black_rook_image, (letter * TILESIZE, number * TILESIZE))
    elif type(piece) == King:
        if piece.color == Color.White:
            board_surf.blit(white_king_image, (letter * TILESIZE, number * TILESIZE))
        else:
            board_surf.blit(black_king_image, (letter * TILESIZE, number * TILESIZE))
    elif type(piece) == Queen:
        if piece.color == Color.White:
            board_surf.blit(white_queen_image, (letter * TILESIZE, number * TILESIZE))
        else:
            board_surf.blit(black_queen_image, (letter * TILESIZE, number * TILESIZE))
    elif type(piece) == Knight:
        if piece.color == Color.White:
            board_surf.blit(white_knight_image, (letter * TILESIZE, number * TILESIZE))
        else:
            board_surf.blit(black_knight_image, (letter * TILESIZE, number * TILESIZE))


def drawing(board_surf):
    for piece in list_of_pieces:
        draw_piece(board_surf, piece.current_position_x, piece.current_position_y, piece)


def main():
    temp1 = None
    pawn = None
    board = create_board()
    place_pieces(board)
    win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    while True:
        board_surf = create_board_surf()
        events = pygame.event.get()
        for e in events:
            if e.type == pygame.QUIT:
                return
            if e.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0] and temp1 is None:
                    if pawn is not None:
                        click_on_promotion_surface(pawn, board)
                    else:
                        temp1 = click_on_board(board)
                elif pygame.mouse.get_pressed()[0]:
                    move_piece(board, temp1)
                    temp1 = None

        win.fill((254, 172, 0))
        pygame.draw.rect(win, (189, 111, 12), (0, 640, 1280, 80))
        pygame.draw.rect(win, (189, 111, 12), (0, 0, 1280, 80))
        if temp1 is not None:
            pygame.draw.rect(board_surf, (0, 255, 0), (temp1.current_position_x * TILESIZE, temp1.current_position_y * TILESIZE, TILESIZE, TILESIZE))
        drawing(board_surf)
        pawn = find_pawn_to_promote(board)
        if pawn is not None:
            check_promotion(board_surf, board)
        check_promotion(board_surf, board)
        win.blit(board_surf, (360, 80))
        pygame.display.flip()
        clock.tick(60)


main()
