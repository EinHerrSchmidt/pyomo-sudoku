from __future__ import division
import pyomo.environ as pyo

model = pyo.AbstractModel()

model.I = pyo.Param(within=pyo.NonNegativeIntegers)
model.J = pyo.Param(within=pyo.NonNegativeIntegers)
model.N = pyo.Param(within=pyo.NonNegativeIntegers)

model.R = pyo.Param(within=pyo.NonNegativeIntegers)
model.C = pyo.Param(within=pyo.NonNegativeIntegers)

model.i = pyo.RangeSet(1, model.I)
model.j = pyo.RangeSet(1, model.J)
model.n = pyo.RangeSet(1, model.N)

model.r = pyo.RangeSet(1, model.R)
model.c = pyo.RangeSet(1, model.C)

model.f = pyo.Param(model.i, model.j)

model.x = pyo.Var(model.i, model.j, model.n, domain=pyo.Binary)


def obj_expression(model):
    return pyo.summation(model.x)


model.obj = pyo.Objective(rule=obj_expression, sense=pyo.maximize)


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


def known_entries_constraint_rule(model, i, j):
    n = model.f[i, j]
    if(n != 0):
        return model.x[i, j, n] == 1
    return model.x[1, 1, 1] == model.x[1, 1, 1]


model.rows = pyo.Constraint(model.n, model.i, rule=rows_constraint_rule)
model.cols = pyo.Constraint(model.n, model.j, rule=columns_constraint_rule)
model.overlap = pyo.Constraint(model.i, model.j, rule=no_overlap_constraint_rule)
model.squares = pyo.Constraint(model.n, model.r, model.c, rule=squares_constraint_rule)
model.fixed = pyo.Constraint(model.i, model.j, rule=known_entries_constraint_rule)

instance = model.create_instance(filename="../data/data.dat")

solver = pyo.SolverFactory('cplex')
solver.solve(instance)

def print_solution():
    for i in instance.i:
        for j in instance.j:
            print(" ", end="")
            for n in instance.n:
                if(instance.x[i, j, n].value == 1):
                    print(n, end="")
        print()


print_solution()