import tkinter as tk
import random
from tkinter import messagebox
import tkinter.simpledialog as sd

class game:
    def __init__(self, xlength, pl_narkes, font):
        self.grid = allGames.grid
        self.font = font
        #global grid, font
        self.root = tk.Tk()
        self.infull_screen = False
        self.root.attributes("-fullscreen", self.infull_screen)
        self.root.resizable(False, False)
        self.xlim = self.root.winfo_screenwidth()
        self.ylim = self.root.winfo_screenheight()
        #self.root.geometry(str(self.xlim)+"x"+str(self.ylim))
        
        self.pl_narkes = pl_narkes
        self.xlength=xlength
        self.side = int(4*self.xlim/(6*self.xlength))
        self.ylength = int((self.ylim-50)/self.side)
        
        rect.closed_rects = self.xlength*self.ylength
        rect.narkes = self.pl_narkes
        
        self.canvas = tk.Canvas(self.root, bg="#404040")
        self.canvas.pack(fill="both", expand=1)

        mb_game = tk.Menubutton(self.canvas, text="Game", font="Arial 12")
        mb_game.pack(anchor="nw")

        menu_game = tk.Menu(mb_game, font="Arial 10")
        menu_game.add_command(label="Start new", command=self.start_new_game)
        menu_game.add_command(label="Score", command=self.print_score)
        menu_game.add_separator()
        menu_game.add_command(label="Go to/Remove full screen", command=self.change_fullscreen)
        menu_game.add_command(label="Έξοδος", command=self.root.destroy)
        mb_game.config(menu=menu_game)
        
        self.fr_game = tk.Frame(self.canvas, height=self.root.winfo_screenheight(), width=self.xlength*self.side)
        self.fr_game.place(x=int(self.xlim/6), y=0, anchor="nw")
        
        self.fr_grid = tk.Frame(self.fr_game, width=self.xlength*self.side, height=(self.ylim-50))
        self.fr_grid.place(x=0, y=0, anchor="nw")

        self.lab_narkes = tk.Label(self.fr_game, text=str(pl_narkes), font="Arial 20")
        self.lab_narkes.place(x=int(self.xlength*self.side/2), y=self.ylim-50, anchor="nw")

        narkes=[]
        for i in range(self.ylength):
            narkes.append([])
            for j in range(self.xlength):
                narkes[-1].append(0)
        for k in range(self.pl_narkes):
            [i, j] = self.coordinates()
            while narkes[i][j]==1:
                [i, j] = self.coordinates()
            narkes[i][j] = 1
        
        for i in range(self.ylength):
            self.grid.append([])
            for j in range(self.xlength):
                color = "#0080ff"
                b = tk.Button(self.fr_grid, bg=color, font=("Helvetica", str(self.font)))
                b.place(x=self.side*j, y=self.side*i, anchor="nw", width=self.side, height=self.side)
                self.grid[-1].append(rect(i, j, narkes[i][j], b, self))

        self.root.mainloop()
    def coordinates(self):
        return [random.randrange(self.ylength), random.randrange(self.xlength)]
    def change_fullscreen(self):
        self.root.attributes("-fullscreen", not self.infull_screen)
        self.infull_screen = not self.infull_screen
    def print_score(self):
        winning_games = allGames.winning_games; losing_games = allGames.losing_games
        messagebox.showinfo("Score", "Wins: "+str(winning_games)+"\nLosts: "+str(losing_games))
    def start_new_game(self):
        ans = messagebox.askquestion("New Game", "Are you sure that you want to stop the current game?",parent=self.root)
        if ans=='no':
            return
        self.root.destroy()
        self.grid=[]
        allGames.start_game()
    def win(self):
        for i in range(self.ylength):
            for j in range(self.xlength):
                if self.grid[i][j].button["state"] != "disabled":
                    self.grid[i][j].button["state"] = "disabled"
                    self.grid[i][j].button["bg"] = "white"
        ans = messagebox.askquestion("Win", "Congrats! You won\nDo you want to play again;", parent=self.root)
        allGames.winning_games += 1
        self.grid = []
        if ans=="yes":
            self.root.destroy()
            allGames.start_game()
        else:
            self.root.destroy()
    def lose(self):
        for i in range(self.ylength):
            for j in range(self.xlength):
                if self.grid[i][j].button["state"] != "disabled":
                    self.grid[i][j].button["state"] = "disabled"
                    if self.grid[i][j].state:
                        self.grid[i][j].button["bg"] = "black"
        ans = messagebox.askquestion("Lost", "You lost!\nDo you want to play again?", parent=self.root)
        allGames.losing_games += 1
        self.grid=[]
        if ans=="yes":
            self.root.destroy()
            allGames.start_game()
        else:
            self.root.destroy()

class allGames:
    grid=[]
    winning_games, losing_games=0, 0
    @staticmethod
    def start_game():
        difficulties=[(10, 10, 30), (20, 30, 25), (20, 40, 25), (20, 50, 25), (30, 70, 16)]
        diff = "a"
        while not diff.isdigit() or int(diff) >= len(difficulties):
            diff = sd.askstring("Difficulty", "Select the difficulty of the game(0-"+str(len(difficulties)-1)+")")
            if diff==None:
                return
        font = difficulties[int(diff)][2]
        allGames.grid=[]
        game(difficulties[int(diff)][0], difficulties[int(diff)][1], font)

class rect:
    foregrounds=["#00cc66", "#ffff00", "#ff3399", "#000066", "#ff3333", "#663300"]
    narkes = None
    closed_rects = None
    def __init__(self, i, j, state, but, app):
        self.grid=app.grid
        self.app = app
        self.i, self.j = i, j
        self.state = state
        self.button = but
        self.button["command"] = self.open_rect
        self.button.bind("<Enter>", self.activate)
        self.button.bind("<Leave>", self.disactivate)
    def disactivate(self, event):
        if self.button["state"] == "disabled":
            return
        self.button["bg"] = "#0080ff"
    def activate(self, event):
        if self.button["state"] == "disabled":
            return
        self.button["bg"] = "blue"
    def open_rect(self):
        global app
        if self.button["state"] == "disabled":
            return
        if self.state:
            game.lose(self.app)
            return
        dy = [1, 1, 1, -1, -1, -1, 0, 0]
        dx = [-1, 0, 1, -1, 0, 1, 1, -1]
        neighboring_narkes = 0
        for i in range(8):
                d1, d2 = dy[i], dx[i]
                if self.i+d1 < 0 or self.i+d1 >= len(self.grid) or self.j+d2 < 0 or self.j+d2 >= len(self.grid[0]):
                    continue
                if self.grid[self.i+d1][self.j+d2].state:
                    neighboring_narkes+=1
        rect.closed_rects-=1
        self.button["state"] = "disabled"
        self.button["bg"] = "#c0c0c0"
        if neighboring_narkes>0:
            self.button["disabledforeground"] = rect.foregrounds[neighboring_narkes-1]
            self.button["text"] = str(neighboring_narkes)
            if rect.closed_rects == rect.narkes:
                self.app.win()
            return
        if rect.closed_rects==rect.narkes:
            self.app.win()
            return
        
        #dfs if neighbors=0
        for i in range(8):
                d1, d2 = dy[i], dx[i]
                if self.i+d1 < 0 or self.i+d1 >= len(self.grid) or self.j+d2 < 0 or self.j+d2 >= len(self.grid[0]):
                    continue
                self.grid[self.i+d1][self.j+d2].open_rect()

#difficulties=[(10, 10, 30), (20, 30, 25), (20, 40, 25), (20, 50, 25), (30, 70, 16)]
#winning_games, losing_games=0, 0
allGames.start_game()
