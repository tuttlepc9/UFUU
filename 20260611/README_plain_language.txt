UFUU — What Is This Project?
A Plain-Language Explanation
W. Jason Tuttle, 2026

============================================================

THE BIG QUESTION

What if the universe isn't made of "stuff" at all? What if
everything — space, time, matter, gravity — is the output of a
single recursive computation? One operation, applied to itself,
over and over, generating everything we see?

That's the question this project is trying to answer.

============================================================

WHAT IS U = F(U, U)?

This is the core equation. It says: the universe (U) is the
result of some operation (F) applied to itself, twice. That's it.
No external inputs. No starting conditions handed down from
outside. Just one function, folding into itself, recursively.

Think of it like this: imagine you have a single rule — like
"take two numbers and combine them." Now apply that rule to its
own output, and then to that output, and so on, billions of
times. What comes out the other end?

It turns out: structure. Organization. Patterns that look
suspiciously like the patterns we see in actual physics.

============================================================

WHAT DOES THE CODE DO?

The Python scripts in this repository implement that idea
computationally. They build a binary tree — a structure that
starts with a huge number of simple values at the bottom and
folds them together, pair by pair, level by level, until a
single value comes out the top.

The "fold function" — the specific rule used to combine two
values into one — is where all the physics lives. Different
fold functions produce different kinds of output. Some produce
spatial structure. Some produce symmetry. Some might produce
something that looks like gravity.

We test four candidate fold functions in the paper:

  1. Golden Ratio Fold — tests whether the universe naturally
     organizes into quasicrystalline patterns (like the atomic
     structure of certain exotic metals).

  2. Modular Arithmetic Fold — tests whether the continuous
     symmetries we see in particle physics can emerge from
     discrete computation.

  3. XOR-Carry Fold — the absolute minimum possible operation,
     testing whether pure information theory alone can produce
     structure.

  4. Mobius Fold — tests whether conformal symmetry (the
     deepest symmetry in fundamental physics, connected to
     Einstein's theory of relativity) emerges naturally.

============================================================

WHAT DO THE RESULTS SHOW?

So far, the golden ratio fold (UFUUGR1) shows:

  - The fold produces organized spatial structure from nothing
    but recursion and a single rule. Values aren't random —
    they form coherent patterns across the grid.

  - Long-range correlations appear with quasi-periodic
    oscillations, consistent with quasicrystalline order.
    The universe this fold builds has large-scale structure,
    not chaos.

  - It does NOT produce gravity-like behavior at the depths
    tested so far. The curvature proxy and energy proxy are
    completely decoupled. This is an honest negative result —
    it tells us the golden ratio fold probably isn't the one
    that generates gravity. The Mobius fold is the next
    candidate to test.

============================================================

WHY DOES THIS MATTER?

Einstein spent the last 30 years of his life trying to find a
single framework that unifies all of physics. He died in 1955
with his calculations on his nightstand, unfinished.

This project approaches the same question from the opposite
direction. Einstein started with the physics and tried to find
the unifying math. This framework starts with the simplest
possible computational architecture and asks: what fold function
reproduces the physics we observe?

If the answer exists — if there is a specific fold function that
generates space, time, matter, and gravity from pure recursion —
then U = F(U, U) is the theory of everything, expressed in seven
characters.

We're not there yet. But the framework is testable, the code is
public, and the results so far show that the architecture
produces nontrivial structure. The fold function is the theory.
Finding it is the work that remains.

============================================================

HOW TO READ THE FIGURES

Each figure in this repository is a four-panel diagnostic:

  Top-left: Summary of the fold function and basic parameters.

  Top-right: Spatial correlation — does the fold produce
  organized structure, or just noise? A flat line means noise.
  A power-law decay with structure means the fold is generating
  spatial order.

  Bottom-left: Gravity test — does the fold produce something
  that looks like Einstein's field equations (R = 8*pi*T)?
  If the blue and red lines track each other, that's a signal.
  If they don't, it's an honest negative result.

  Bottom-right: A heatmap of the fold's output mapped to a 2D
  grid. Organized patterns = the fold is building spatial
  structure. Random static = the fold isn't doing anything
  interesting.

============================================================

CAN I RUN THE CODE?

Yes. Everything here is standard Python (NumPy, Matplotlib,
SciPy). Clone the repo, install the dependencies, and run any
of the scripts. They produce the figures you see in the
repository. The results are deterministic — you will get
exactly the same output every time.

  pip install numpy matplotlib scipy
  python UFUUGR1.py

============================================================

WHERE IS THE PAPER?

The formal academic paper describing this framework has been
submitted to Foundations of Physics (Springer) and is available
as a preprint on Research Square.

Tuttle, W.J. (2026). Recursive Fold Architectures for Self-
Generating Systems: A Minimal Viable Framework with Candidate
Fold Functions, Constraint Sequencing, and Testable Predictions.

============================================================

Repository: https://github.com/tuttlepc9/UFUU
Contact: mail@jasontuttle.com
