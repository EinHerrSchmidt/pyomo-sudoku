from __future__ import division
import pyomo.environ as pyo
from data_maker import DataMaker


def obj_expression(model):
    return pyo.summation(model.x)


def rows_constraint_rule(model, n, i):
    return sum(model.x[i, j, n]for j in model.j) == 1


def columns_constraint_rule(model, n, j):
    return sum(model.x[i, j, n]for i in model.i) == 1


def no_overlap_constraint_rule(model, i, j):
    return sum(model.x[i, j, n]for n in model.n) == 1


def squares_constraint_rule(model, n, r, c):
    i_range = pyo.RangeSet(3 * r - 2, 3 * r)
    j_range = pyo.RangeSet(3 * c - 2, 3 * c)
    return sum(model.x[i, j, n] for i in i_range for j in j_range) == 1


class SudokuSolver:

    def __init__(self):
        self.dataMaker = DataMaker()
        self.model = pyo.AbstractModel()
        self.initialize_model()

    def initialize_model(self):
        self.model.I = pyo.Param(within=pyo.NonNegativeIntegers)
        self.model.J = pyo.Param(within=pyo.NonNegativeIntegers)
        self.model.N = pyo.Param(within=pyo.NonNegativeIntegers)
        self.model.R = pyo.Param(within=pyo.NonNegativeIntegers)
        self.model.C = pyo.Param(within=pyo.NonNegativeIntegers)

        self.model.i = pyo.RangeSet(1, self.model.I)
        self.model.j = pyo.RangeSet(1, self.model.J)
        self.model.n = pyo.RangeSet(1, self.model.N)
        self.model.r = pyo.RangeSet(1, self.model.R)
        self.model.c = pyo.RangeSet(1, self.model.C)

        self.model.x = pyo.Var(self.model.i,
                               self.model.j,
                               self.model.n,
                               domain=pyo.Binary)

        self.model.obj = pyo.Objective(rule=obj_expression, sense=pyo.maximize)

        self.model.rows = pyo.Constraint(
            self.model.n,
            self.model.i,
            rule=rows_constraint_rule)
        self.model.cols = pyo.Constraint(
            self.model.n,
            self.model.j,
            rule=columns_constraint_rule)
        self.model.overlap = pyo.Constraint(
            self.model.i,
            self.model.j,
            rule=no_overlap_constraint_rule)
        self.model.squares = pyo.Constraint(
            self.model.n,
            self.model.r,
            self.model.c,
            rule=squares_constraint_rule)

    def fix_variables(self, sudokuGrid):
        for i in range(0, 9):
            for j in range(0, 9):
                n = sudokuGrid[i][j]
                if(n != 0):
                    self.instance.x[i+1, j+1, n].fix(1)

    def solve(self, sudokuGrid):
        self.instance = self.model.create_instance(
            self.dataMaker.make_indices())
        self.fix_variables(sudokuGrid)

        solver = pyo.SolverFactory('cplex')
        solver.solve(self.instance)
        return self.extractSolution(self.instance)

    def extractSolution(self, instance):
        solutionGrid = [[0 for i in range(0, 9)] for j in range(0, 9)]
        for i in instance.i:
            for j in instance.j:
                for n in instance.n:
                    if(instance.x[i, j, n].value == 1):
                        solutionGrid[i-1][j-1] = n
        return solutionGrid

    def print_solution(self, instance):
        for i in instance.i:
            for j in instance.j:
                print(" ", end="")
                for n in instance.n:
                    if(instance.x[i, j, n].value == 1):
                        print(n, end="")
            print()
