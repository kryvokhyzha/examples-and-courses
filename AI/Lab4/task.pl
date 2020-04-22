:- dynamic jars/2.
solve(jar(VolumeA, A), jar(VolumeB, B), jar(VolumeC, C), target(Target), Actions):-
  retractall(jars(_, _, _)),
  bfs(volumes(VolumeA, VolumeB, VolumeC), target(Target), [state(jars(A, B, C), actions([init]))], Actions).
  
bfs(_Volumes, target(Target), [state(jars(A, B, C), Actions)|_Other], Actions):-
  ((A = Target, B = Target); (A = Target, C = Target); (B = Target, C = Target)).
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
  NextState = state(jars(A, B, C), _Actions),
  \+ jars(A, B, C),
  assert(jars(A, B, C)).
  
next_state(volumes(VolumeA, VolumeB, VolumeC), jars(A, B, C), actions(PrevActions), NextState):-
  ((\+ B = 0), (\+ A = VolumeA)) , % из B можно перелить в A 
  APlusB is min((A + B), VolumeA), % A = A + B
  Delta is APlusB - A, % сколько смогли перелить
  BMinusDelta is B - Delta, % B = B - Delta
  NextState = state(jars(APlusB, BMinusDelta, C), actions([из_B_в_A|PrevActions]));
  
  ((\+ B = 0), (\+ C = VolumeC)), % из B можно перелить в C
  CPlusB is min((C + B), VolumeC), % C = C + B
  Delta is CPlusB - C, % сколько смогли перелить
  BMinusDelta is B - Delta, % B = B - Delta
  NextState = state(jars(A, BMinusDelta, CPlusB), actions([из_B_в_C|PrevActions]));
  
  ((\+ A = 0), (\+ B = VolumeB)), % из A можно перелить в B
  BPlusA is min((A + B), VolumeB), % B = B + A
  Delta is BPlusA - B, % сколько смогли перелить
  AMinusDelta is A - Delta, 
  NextState = state(jars(AMinusDelta, BPlusA, C), actions([из_А_в_В|PrevActions]));

  ((\+ A = 0), (\+ C = VolumeC)), % из A можно перелить в C
  CPlusA is min((A + C), VolumeC), % C = C + A
  Delta is CPlusA - C, % сколько смогли перелить
  AMinusDelta is A - Delta, 
  NextState = state(jars(AMinusDelta, B, CPlusA), actions([из_А_в_C|PrevActions]));

  ((\+ C = 0), (\+ B = VolumeB)), % из C можно перелить в B
  BPlusC is min((C + B), VolumeB), % B = B + C
  Delta is BPlusC - B, % сколько смогли перелить
  CMinusDelta is C - Delta, 
  NextState = state(jars(A, BPlusC, CMinusDelta), actions([из_C_в_В|PrevActions]));

  ((\+ C = 0), (\+ A = VolumeA)), % из C можно перелить в A 
  APlusC is min((A + C), VolumeA), % A = A + C
  Delta is APlusC - A, % сколько смогли перелить
  CMinusDelta is C - Delta, % C = C - Delta
  NextState = state(jars(APlusC, B, CMinusDelta), actions([из_C_в_A|PrevActions])).
  

