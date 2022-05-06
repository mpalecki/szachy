# szachy

1. Program tworzy listę, która będzie spełniać funkcję szachownicy i przypisuje ją do zmiennej board (create_board())
2. W funkcji place_pieces(board) tworzone są figury i ustawiane na szachownicy. Wykorzystuję do tego słownik piece_type.
3. Potem program tworzy okno i zegar. 
4. W głownej pętli rysowana jest szachownica (create_board_surf()) i sprawdzane są eventy.
5. Przy kliknięciu na okno program sprawdza, czy użytkownik klikną w szachownicę i czy na wskazanym przez niego polu jest jakaś figura.
  Jeśli tak, to dodana jest ona do zmiennej temp1. Przy następnym kliknięciu, gdy temp1 ma wartość, program sprawdza, czy wskazane pole jest puste
  i, jeśli pozwalają na to zasady gry, przesuwa na nie figurę. Przy okazji sprawdzane też jest, czy ruszana figura nie jest pionem (pawn) przesuniętym
  na ostatnią linię. W takim wypadku pojawia się pole wyboru promocji piona.
6. Po wykonanym ruchu pętla rysuje wszystkie figury znajdujące się na szachownicy.
7. Przesuwanie figur - przy ruchu program sprawdza najpierw, czy jest on dozwolony. Zaczyna od znalezienia króla (find_king(current_turn))
  i sprawdzenia, czy nie jest on szachowany. Jeśli jest, program ustala, użytkownik próbuje zbić królem szachującą figurę (capture), przesunąć się 
  królem na nieszachowane pole bądź zasłonić króla którąś z figur. Jeżeli żadne z tych, ruch się nie wykonuje. 
  Następnie, jeśli nie ma szacha, sprawdzane jest, czy użytkownik próbuje zrobić roszadę. Jeżeli tak i obu figurom pozwala na to pole can_castle, 
  roszada wykonuje się (castling). 
  W innym przypadku program ustala, czy użytkownik rusza na puste pole i czy figura może się w ten sposób poruszać (can_move). Jeśli występuje próba 
  ruchu na pole figury przeciwnika, następuje zbicie i dana figura zostaje usunięta z list_of_pieces, czyli listy figur obecnych w grze.
  Przy zbijaniu występuje jeszcze funkcja can_capture, ale jej wartość jest równa funkcji can_move przy każdej figurze oprócz piona.
  Pod koniec funkcji move_piece znajdują się is_check i is_checkmate. Pierwsza sprawdza czy istnieją figury szachujące króla i dodaje je do listy checkers.
  Druga oblicza pola między królem a figurą szachującą (find_fields_between) i ustala, czy możliwy jest ruch figury koloru króla, by go zasłonić.
  Następnie sprawdza, czy możliwy jest ruch królem na nieszachowane pole. Jeśli w obu wypadkach otrzymano False i król jest obecnie szachowany, current_turn
  zmienia się na None, by żadna ze stron nie mogła już wykonywać ruchów i gra kończy się. 
8. Każda z figur ma metodę is_patch_clear, która sprawdza, czy przy próbie ruchu "droga" między aktualnym polem i polem docelowym jest pusta.
9. Color jest Enumem ze nadpisaną negacją, aby możliwe były tylko wartości White i Black (oraz None na koniec gry).
