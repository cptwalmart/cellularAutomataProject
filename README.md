# cellularAutomataProject

A representation of one dimensional finite cellular automata in Python 3.6.8.

Cellular automata, in this project, are array based dynamical systems, meaning that they map changes over discrete time steps, eg. T = 0, 1, 2, 3,..., N. The underlying structure behind these automata is a finite set of cells in a lattice up to a user defined dimension (dimension, in this case, referring to the number of columns, as in a matrix).

We use a finite alphabet, starting at 0 and ending at a user defined number.

Every automaton requires an update rule, which defines how the states will evolve to the next state. This rule will usually be of the form A + B + C + ... + N, where A...N are cells in the previous state.

Boundary conditions often affect how states will evolve, depending on the update rule. They answer the question of 'What do end cells connect to?'
  Null Boundary condition - end cells are connected to logic 0 state, eg the state 1111 can be compared to 011110.
  Periodic Boundary condition - end cells are connected to opposite end cells, eg the state 1001 can be compared to 110011.
For the sake of our project, we will be using periodic boundary conditions.

The main purpose of this project is to be able to find and manipulate cycles in cellular automata. As these automata are finite, they will eventually reach a cycle, meaning a set of states that has already been evolved to in an automaton.

  0001        0001        0001
  0010        1001        0011
  0100        0101        1100
  1000        1111*       1110
  0001*       1111*       0110
  0010*       1111*       0111
  
In the above examples, as the first column evolves, we reach a cycle at state 5, and the automaton begins to repeat itself. As the second column evolves, we reach a cycle at state 4, and the automaton cycles through the same state (1111) infinitely. The third column has no discernable cycle in the given 7 states, but since the automaton is finite, it will eventually reach a cycle. Considering the alphabet {0,1}, there are 2^4 possible states, meaning that if you evolve any of these automata over 2^4 +1 states (17), you are guaranteed to find a cycle.


More information will follow.





