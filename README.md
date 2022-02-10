# pyomo-sudoku

A linear programming based Sudoku solver.

# Model

Have a look [here](model_description.ipynb) for an explanation of the model.

# Execution

Simply launch `python sudoku_abstract.py` in order to execute the solver, or `python sudoku_abstract.py > result.txt` if you prefer to redirect the solver's output to a file.

**Remark**: this implementation assumes the availability of IBM's CPLEX solver. It can easily be changed to any other available LP solver.