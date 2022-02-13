import tkinter as Tk


class View():
    def __init__(self, master, controller):
        self.controller = controller
        self.frame = Tk.Frame(master)
        self.frame.pack()
        self.viewPanel = ViewPanel(master, controller)


class ViewPanel():
    def __init__(self, root, controller):
        self.controller = controller

        self.sudokuFrame = Tk.Frame(root)
        self.sudokuFrame.pack()

        self.entries = [[None for i in range(0, 9)] for j in range(0, 9)]
        self.stringVars = [[None for i in range(0, 9)] for j in range(0, 9)]
        for i in range(0, 9):
            for j in range(0, 9):
                sv = Tk.StringVar(self.sudokuFrame)
                sv.trace_add("write",
                             lambda x1, x2, x3, sv=sv, i=i, j=j: self.controller.insertValue(sv, i, j))
                entry = Tk.Entry(self.sudokuFrame,
                                 width=2,
                                 highlightthickness=1,
                                 highlightbackground='#000000',
                                 justify='center',
                                 font=('Courier 18'),
                                 textvariable=sv)
                self.entries[i][j] = entry
                self.entries[i][j].grid(row=i, column=j, ipadx=5, ipady=5)
                self.stringVars[i][j] = sv

        solveButton = Tk.Button(root, text="Solve!", width=8, height=2)
        solveButton.bind("<Button-1>", lambda event: self.controller.solve())
        solveButton.pack()

        resetButton = Tk.Button(root, text="Reset!", width=8, height=2)
        resetButton.bind("<Button-1>", lambda event: self.controller.reset())
        resetButton.pack()
