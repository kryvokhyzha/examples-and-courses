


bestfirst( Start, Solution) :-
  expand( [], l( Start, 0/0),  9999, _, yes, Solution).

% --------- 1

expand( P, l( N, _), _, _, yes, [N|P])  :-
   goal(N).


% --------- 2

expand( P, l(N,F/G), Bound, Tree1, Solved, Sol)  :-
  F  =<  Bound,
  (  bagof( M/C, (s(N,M,C), not(member(M,P))), Succ), 
     !,                                    % Node N has successors
     succlist( G, Succ, Ts),               % Make subtrees Ts
     bestf( Ts, F1),                       % f-value of best successor	
     expand( P, t(N,F1/G,Ts), Bound, Tree1, Solved, Sol)
     ;
     Solved = never
  ) .

% --------- 3

expand( P, t(N,F/G,[T|Ts]), Bound, Tree1, Solved, Sol)  :-
  F  =<  Bound,
  bestf( Ts, BF), min( Bound, BF, Bound1),          % Bound1 = min(Bound,BF)
  expand( [N|P], T, Bound1, T1, Solved1, Sol),
  continue( P, t(N,F/G,[T1|Ts]), Bound, Tree1, Solved1, Solved, Sol).

% --------- 4

expand( _, t(_,_,[]), _, _, never, _) :- !.

% --------- 5

expand( _, Tree, Bound, Tree, no, _)  :-
  f( Tree, F), F > Bound.

% continue( Path, Tree, Bound, NewTree, SubtreeSolved, TreeSolved, Solution)

continue( _, _, _, _, yes, yes, Sol).

continue( P, t(N,F/G,[T1|Ts]), Bound, Tree1, no, Solved, Sol)  :-
  insert( T1, Ts, NTs),
  bestf( NTs, F1),
  expand( P, t(N,F1/G,NTs), Bound, Tree1, Solved, Sol).

continue( P, t(N,F/G,[_|Ts]), Bound, Tree1, never, Solved, Sol)  :-
  bestf( Ts, F1),
  expand( P, t(N,F1/G,Ts), Bound, Tree1, Solved, Sol).



% --------- 6 
% succlist( G0, [ Node1/Cost1, ...], [ l(BestNode,BestF/G), ...]):

succlist( _, [], []).

succlist( G0, [N/C | NCs], Ts)  :-
  G is G0 + C,
  h( N, H),                             % Heuristic term h(N)
  F is G + H,
  succlist( G0, NCs, Ts1),
  insert( l(N,F/G), Ts1, Ts).

% --------- 7

insert( T, Ts, [T | Ts])  :-
  f( T, F), bestf( Ts, F1),
  F  =<  F1, !.

insert( T, [T1 | Ts], [T1 | Ts1])  :-
  insert( T, Ts, Ts1).


% Extract f-value

f( l(_,F/_), F).        % f-value of a leaf

f( t(_,F/_,_), F).      % f-value of a tree

bestf( [T|_], F)  :-    % Best f-value of a list of trees
  f( T, F).

bestf( [], 9999).       % No trees: bad f-value
  
min( X, Y, X)  :-
  X  =<  Y, !.

min( X, Y, Y).



s([Empty | Tiles], [Tile | Tiles1], 1):-  % Стоимости всех дуг равны 1
  swap(Empty, Tile, Tiles, Tiles1).         % Поменять местами пустую фишку 
					% Empty и фишку Tile в списке Tiles

swap(Empty, Tile, [Tile | Ts], [Empty | Ts] ):-
  mandist( Empty, Tile, 1).                  % Манхэттенское расстояние равно 1

swap( Empty, Tile, [T1 | Ts], [T1 | Ts1] )  :-
  swap( Empty, Tile, Ts, Ts1).

mandist( X/Y, X1/Y1, D)  :-          % D - это манхэттенское расстояние между двумя клетками
  dif( X, X1, Dx),
  dif( Y, Y1, Dy),
  D is Dx + Dy.

dif( A, B, D)  :-              % D is |A-B|
  D is A-B, D >= 0, !
  ;
  D is B-A.


h( [Empty | Tiles], H)  :-
  goal( [Empty1 | GoalSquares] ),
  totdist( Tiles, GoalSquares, D),      % Суммарное расстояние от исходных клеток
  seq( Tiles, S),                       % Оценка упорядоченности
  H is D + 3*S.

totdist( [], [], 0).

totdist( [Tile | Tiles], [Square | Squares], D)  :-
  mandist( Tile, Square, D1),
  totdist( Tiles, Squares, D2),
  D is D1 + D2.

% seq( TilePositions, Score): оценка упорядоченности

seq( [First | OtherTiles], S)  :-
  seq( [First | OtherTiles ], First, S).

seq( [Tile1, Tile2 | Tiles], First, S)  :-
  score( Tile1, Tile2, S1),
  seq( [Tile2 | Tiles], First, S2),
  S is S1 + S2.

seq( [Last], First, S)  :-
  score( Last, First, S).

score( 2/2, _, 1)  :-  !.              % ценка фишки, стоящей в центре, равна 1

score( 1/3, 2/3, 0)  :-  !.            % Оценка фишки, за которой следует допустимый преемник, равна 0
score( 2/3, 3/3, 0)  :-  !.
score( 3/3, 3/2, 0)  :-  !.
score( 3/2, 3/1, 0)  :-  !.
score( 3/1, 2/1, 0)  :-  !.
score( 2/1, 1/1, 0)  :-  !.
score( 1/1, 1/2, 0)  :-  !.
score( 1/2, 1/3, 0)  :-  !.

score( _, _, 2).                       % Оценка фишкк, за которой следует недопустимый преемник, равна 2

goal( [2/2,1/3,2/3,3/3,3/2,3/1,2/1,1/1,1/2] ).  % Goal squares for tiles





