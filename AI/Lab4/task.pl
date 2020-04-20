:- dynamic jars/2.
solve(jar(VolumeA, A), jar(VolumeB, B), target(Target), Actions):-
  retractall(jars(_, _)),
  bfs(volumes(VolumeA, VolumeB), target(Target), [state(jars(A, B), actions([init]))], Actions).
  
bfs(_Volumes, target(Target), [state(jars(A, B), Actions)|_Other], Actions):-
  (A = Target; B = Target).
bfs(Volumes, target(Target), [state(Jars, HeadActions)|Buffer], Actions):-
  generate_states(Volumes, Jars, HeadActions, NextStates),
  append(Buffer, NextStates, NextBuffer),
  bfs(Volumes, target(Target), NextBuffer, Actions).
  
generate_states(Volumes, Jars, actions(PrevActions), NextStates):-
  findall(NextState, 
          next_unique_state(Volumes, Jars, actions(PrevActions), NextState),
          NextStates).
          
next_unique_state(Volumes, Jars, PrevActions, NextState):-
  next_state(Volumes, Jars, PrevActions, NextState),
  NextState = state(jars(A, B), _Actions),
  \+ jars(A, B),
  assert(jars(A, B)).
  
next_state(volumes(VolumeA, VolumeB), jars(A, B), actions(PrevActions), NextState):-
  \+ B = 0, % из B можно перелить в A 
  APlusB is min((A + B), VolumeA), % A = A + B
  Delta is APlusB - A, % сколько смогли перелить
  BMinusDelta is B - Delta, % B = B - Delta
  NextState = state(jars(APlusB, BMinusDelta), actions([из_B_в_A|PrevActions]));
  
  \+ B = 0, % из B можно вылить
  NextState = state(jars(A, 0), actions([из_В_в_бочку|PrevActions]));
  
  \+ A = 0, % из A можно перелить в B
  BPlusA is min((A + B), VolumeB), % A = A + B
  Delta is BPlusA - B, % сколько смогли перелить
  AMinusDelta is A - Delta, 
  NextState = state(jars(AMinusDelta, BPlusA), actions([из_А_в_В|PrevActions]));
  
  \+ A = 0, % из A можно вылить
  NextState = state(jars(0, B), actions([из_А_в_бочку|PrevActions]));
  
  \+ B = VolumeB, % в B можно зачерпнуть
  NextState = state(jars(A, VolumeB), actions([налить_в_В|PrevActions]));
  
  \+ A = VolumeA, % в A можно зачерпнуть
  NextState = state(jars(VolumeA, B), actions([налить_в_А|PrevActions])).
