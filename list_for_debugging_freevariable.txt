List for working solutions and solutions partially correct.


Working solutions:

- 9x9 mod 2 example is correct.
- 6x6 mod 5 example is correct.
- 8x8 mod 3 example is correct.


Solutions partially correct:

* 7x7 mod 3:
----------------------
+ 1-1 cycle is correct.
- 2-44 cycles is not correct. (Bardzell said that this set should not even show this as output for cycle stats)
+ 13-56 cycles are correct. (This is the longest cycle within this system; no others should be shown after this which is already correct)


* 5x5 mod 5:
---------------------
+ 1-1 cycle is correct.
+ 6-4 cycles is correct.
** (We have solutions for this example now) missing 155-20 cycles as final output. (Only this cycle stat is missing and no others are missing. so in total: 3).
(Need to put a catch in code that determines everything is in the nullspace.)

* 9x9 mod 3: (Extreme irreversible case)
---------------------
+ 1-1 cycle is correct.
Bardzell's explanation in email: "only one 1-cycle.
Every state in this system eventually evolves to the zero state so it is the only cycle."
