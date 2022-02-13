import tkinter as Tk
from model import Model
from sudoku_solver import SudokuSolver
from view import View


class Controller():
    def __init__(self):
        self.sudokuSolver = SudokuSolver()

        self.root = Tk.Tk()
        self.model = Model()
        self.view = View(self.root, self)
        self.root.title("Sudoku")
        self.root.mainloop()

    def insertValue(self, sv: Tk.StringVar, i, j):
        content = sv.get()
        if not content.isdigit():
            sv.set('')
            return
        sv.set('')
        sv.set(content[-1])

        self.model.sudokuGrid[i][j] = int(content[-1])

    def solve(self):
        self.model.sudokuGrid = self.sudokuSolver.solve(self.model.sudokuGrid)
        for i in range(0, 9):
            for j in range(0, 9):
                self.view.viewPanel.stringVars[i][j].set(
                    self.model.sudokuGrid[i][j])

    def reset(self):
        self.model = Model()
        for i in range(0, 9):
            for j in range(0, 9):
                self.view.viewPanel.stringVars[i][j].set('')
