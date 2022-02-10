# pyomo-sudoku

A linear programming based Sudoku solver.

# Model

The model used to solve a generic instance of a 9 by 9 Sudoku is the following:
$\begin{align}
    & \max z = \sum_{i \in I}\sum_{j \in J}\sum_{n \in N} x_{ijn}        
\end{align}$
$\text{subject to:}\\$
$\begin{align}
    & \quad \sum_{j=1}^{9} x_{ijn} = 1, \forall i, \forall n   \\
    & \quad \sum_{i=1}^{9} x_{ijn} = 1, \forall j, \forall n   \\
    & \quad \sum_{i=3r - 2}^{3r}\sum_{j=3c - 2}^{3c} x_{ijn} = 1, \forall n, \forall r, \forall c   \\
    & \quad \sum_{n=1}^{9} x_{ijn} = 1, \forall i, \forall j   \\
\end{align}
$
where $i, j$ and $n$ vary in $\{1, \dots ,9\}$, whereas $r$ and $c$ vary in $\{1, \dots ,3\}$.
The binary variables $x_{ijn}$ are equal to $1$ if cell $(i, j)$ takes value $n$, and $0$ otherwise.
Constraints $(2)$ impose that each value $n$ appears only once in a row; constraints $(3)$ impose that each value $n$ appears only once in a column; constraints $(4)$ impose that each value $n$ appears only once in a $3$ by $3$ sub-square; finally, constraints $(5)$ impose that no values assignments overlap.
Notice that the objective function in $(1)$ could also have been set constant. This formulation has been chosen in order not to cause Pyomo to emit warnings.
A data.dat file is used to set parameters properly. Furthermore, it allows to fix some (or all, although it may not be useful) of the variables' values in order to solve a non-empty grid. This is done via parameter f.

# Execution

Simply launch `python sudoku_abstract.py` in order to execute the solver, or `python sudoku_abstract.py > result.txt` if you prefer to redirect the solver's output to a file.

**Remark**: this implementation assumes the availability of IBM's CPLEX solver. It can easily be changed to any other available LP solver.