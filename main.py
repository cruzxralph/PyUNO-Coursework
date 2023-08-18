from tkinter import *
import sqlite3
from PIL import ImageTk, Image

from game_menu import MenuScreen


def show_frame(frame):
    frame.tkraise()

window = Tk()
window.configure(background="red")
window.state('zoom')
window.geometry("800x800")
window.title("Login")

nameVar = StringVar()
passVar = StringVar()
pythonVar = IntVar()

window.rowconfigure(0, weight=1)
window.columnconfigure(0, weight=1)


def play():
    window.configure(background="red")
    game_menu = MenuScreen(window)
    window.mainloop()
    score = game_menu.score
    print(score)
    show_frame(main_menu)


# method to add user register data in database
def addNew():
    name = nameVar.get()
    password = passVar.get()
    conn = sqlite3.connect("StudentDatabase1.db")
    with conn:
        cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS StudentTable (Name TEXT,Password Text)")
    count = cursor.execute(
        "INSERT INTO StudentTable (Name,Password) VALUES(?,?)", (name, password)
    )

    if cursor.rowcount > 0:
        Label(
            register,
            text="Registration successful",
            bg="red",
            fg="green",
            font=("Calibri", 12, "bold"),
        ).place(relx=0.51, rely=0.5, anchor=CENTER)
    else:
        Label(
            register,
            text="Registration unsuccessful",
            bg="red",
            fg="green",
            font=("Calibri", 12, "bold"),
        ).place(relx=0.51, rely=0.5, anchor=CENTER)
    conn.commit()


# method to perform login
def loginNow():
    name = nameVar.get()
    password = passVar.get()

    conn = sqlite3.connect("StudentDatabase1.db")
    with conn:
        cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS StudentTable (Name TEXT,Password Text)")
    cursor.execute(
        "Select * from StudentTable Where NAME=? AND Password=?", (name, password)
    )

    if cursor.fetchone() is not None:
        print("Welcome")
        show_frame(main_menu)
    else:
        Label(
            login,
            text="Login failed",
            bg="red",
            fg="green",
            font=("Calibri", 12, "bold"),
        ).place(relx=0.51, rely=0.7, anchor=CENTER)

    conn.commit()


class BaseFram(Frame):
    def __init__(self):
        super().__init__(window)
        self.configure(background="red")


# ================================== Login Window
class Login(BaseFram):
    def __init__(self):
        super().__init__()
        Label(
            self,
            text="UNO!",
            bg="red",
            fg="black",
            width="115",
            height="2",
            font=("Calibri", 100, "bold"),
        ).place(relx=0.51, rely=0.1, anchor=CENTER)
        Label(
            self,
            text="Login Here",
            width=20,
            bg="yellow",
            fg="black",
            font=("Calibri", 25, "bold"),
        ).place(relx=0.51, rely=0.275, anchor=CENTER)
        # Username label
        Label(
            self, text="Username:", width=20, bg="red", font=("Calibri", 16, "bold")
        ).place(relx=0.425, rely=0.35, anchor=CENTER)
        Entry(self, font=("Calibri", 16), borderwidth=0, textvar=nameVar).place(
            relx=0.525, rely=0.35, anchor=CENTER
        )
        # Password label
        Label(
            self, text="Password:", width=20, bg="red", font=("Calibri", 16, "bold")
        ).place(relx=0.425, rely=0.4, anchor=CENTER)
        Entry(
            self, font=("Calibri", 16), borderwidth=0, textvar=passVar, show="*"
        ).place(relx=0.525, rely=0.4, anchor=CENTER)
        Button(
            self,
            text="Login",
            font=("Calibri", 12, "bold"),
            bg="yellow",
            borderwidth=0,
            width=20,
            height=2,
            command=loginNow,
        ).place(relx=0.51, rely=0.45, anchor=CENTER)
        Button(
            self,
            text="Don't have an account?",
            font=("Calibri", 12, "bold"),
            bg="red",
            fg="#0000EE",
            borderwidth=0,
            width=20,
            height=1,
            command=lambda: show_frame(register),
        ).place(relx=0.51, rely=0.5, anchor=CENTER)


# ================================== Register Window
class Register(BaseFram):
    def __init__(self):
        super().__init__()
        Label(
            self,
            text="UNO!",
            bg="red",
            fg="black",
            width="115",
            height="2",
            font=("Calibri", 100, "bold"),
        ).place(relx=0.51, rely=0.1, anchor=CENTER)
        Label(
            self,
            text="Registration Here",
            width=20,
            bg="yellow",
            fg="black",
            font=("Calibri", 25, "bold"),
        ).place(relx=0.51, rely=0.275, anchor=CENTER)
        Label(
            self, text="Username:", width=20, bg="red", font=("Calibri", 16, "bold")
        ).place(relx=0.425, rely=0.35, anchor=CENTER)
        Entry(self, font=("Calibri", 16), borderwidth=0, textvar=nameVar).place(
            relx=0.525, rely=0.35, anchor=CENTER
        )
        Label(
            self, text="Password", width=20, bg="red", font=("Calibri", 16, "bold")
        ).place(relx=0.425, rely=0.4, anchor=CENTER)
        Entry(
            self, font=("Calibri", 16), borderwidth=0, textvar=passVar, show="*"
        ).place(relx=0.525, rely=0.4, anchor=CENTER)
        Button(
            self,
            text="Submit",
            font=("Calibri", 12, "bold"),
            bg="yellow",
            borderwidth=0,
            width=20,
            height=2,
            command=addNew,
        ).place(relx=0.51, rely=0.45, anchor=CENTER)
        Button(
            self,
            text="Back to login",
            font=("Calibri", 8, "bold"),
            bg="yellow",
            borderwidth=0,
            width=20,
            height=2,
            command=lambda: show_frame(login),
        ).place(relx=0.51, rely=0.6, anchor=CENTER)


# =====================Main menu code


class MainMenu(BaseFram):
    def __init__(self):
        super().__init__()
        Label(
            self,
            text="UNO!",
            bg="red",
            fg="black",
            width="115",
            height="2",
            font=("Calibri", 100, "bold"),
        ).place(relx=0.51, rely=0.35, anchor=CENTER)
        Button(
            self,
            text="Play",
            borderwidth=0,
            bg="yellow",
            height="2",
            width="30",
            font=("Calibri", 11, "bold"),
            command=lambda: play(),
        ).place(relx=0.51, rely=0.5, anchor=CENTER)
        Button(
            self,
            text="Shop",
            borderwidth=0,
            bg="yellow",
            height="2",
            width="30",
            font=("Calibri", 11, "bold"),
            command=lambda: show_frame(shop),
        ).place(relx=0.51, rely=0.575, anchor=CENTER)
        Button(
            self,
            text="Achievements",
            borderwidth=0,
            bg="yellow",
            height="2",
            width="30",
            font=("Calibri", 11, "bold"),
            command=lambda: show_frame(achievement),
        ).place(relx=0.51, rely=0.65, anchor=CENTER)
        Button(
            self,
            text="Leaderboard",
            borderwidth=0,
            bg="yellow",
            height="2",
            width="30",
            font=("Calibri", 11, "bold"),
            command=lambda: show_frame(leaderboard),
        ).place(relx=0.51, rely=0.725, anchor=CENTER)
        Button(
            self,
            text="Help",
            borderwidth=0,
            bg="yellow",
            height="2",
            width="30",
            font=("Calibri", 11, "bold"),
            command=lambda: show_frame(help),
        ).place(relx=0.51, rely=0.8, anchor=CENTER)


class Shop(BaseFram):
    def __init__(self):
        super().__init__()
        Button(
            self,
            text="Go back",
            borderwidth=0,
            bg="yellow",
            height="2",
            width="30",
            font=("Calibri", 11, "bold"),
            command=lambda: show_frame(main_menu),
        ).place(relx=0.01, rely=0.01, anchor=NW)


# ==================Achievements code
class Achievements(BaseFram):
    def __init__(self):
        super().__init__()
        Button(
            self,
            text="Go back",
            borderwidth=0,
            bg="yellow",
            height="2",
            width="30",
            font=("Calibri", 11, "bold"),
            command=lambda: show_frame(main_menu),
        ).place(relx=0.01, rely=0.01, anchor=NW)


# ==================Leaderboard code
class Leaderboard(BaseFram):
    def __init__(self):
        super().__init__()
        Button(
            self,
            text="Go back",
            borderwidth=0,
            bg="yellow",
            height="2",
            width="30",
            font=("Calibri", 11, "bold"),
            command=lambda: show_frame(main_menu),
        ).place(relx=0.01, rely=0.01, anchor=NW)
        Label(self, borderwidth=0, width=50, height=60, bg="yellow").place(
            relx=0.35, rely=0.5, anchor=CENTER
        )
        Label(self, borderwidth=0, width=50, height=60, bg="yellow").place(
            relx=0.65, rely=0.5, anchor=CENTER
        )
        Label(
            self,
            borderwidth=0,
            text="Top Wins",
            font=("Calibri", 30, "bold"),
            bg="yellow",
        ).place(relx=0.65, rely=0.1, anchor=CENTER)
        Label(
            self,
            borderwidth=0,
            text="Most Coins",
            font=("Calibri", 30, "bold"),
            bg="yellow",
        ).place(relx=0.35, rely=0.1, anchor=CENTER)


# ======================================================================================================================#
# ==================Help code
class Help(BaseFram):
    def __init__(self):
        super().__init__()
        Label(
            self,
            text="Tutorial",
            bg="red",
            fg="black",
            width="115",
            height="2",
            font=("Calibri", 100, "bold"),
        ).place(relx=0.51, rely=0.1, anchor=CENTER)
        Button(
            self,
            text="Go back",
            borderwidth=0,
            bg="yellow",
            height="2",
            width="30",
            font=("Calibri", 11, "bold"),
            command=lambda: show_frame(main_menu),
        ).place(relx=0.01, rely=0.01, anchor=NW)
        Label(
            self,
            text="Play a card to match the colour, number, or symbol on the card.",
            bg="yellow",
            height="5",
            width="60",
            font=("Calibri", 20, "bold"),
        ).place(relx=0.25, rely=0.5, anchor=CENTER)
        self.img = ImageTk.PhotoImage(Image.open("match.png"))
        Label(self, image=self.img).place(relx=0.7, rely=0.5, anchor=CENTER)
        Button(
            self,
            text="Next",
            borderwidth=0,
            bg="yellow",
            height="2",
            width="30",
            font=("Calibri", 11, "bold"),
            command=lambda: show_frame(help2),
        ).place(relx=0.925, rely=0.975, anchor=S)


# =================Second Help window
class Help2(BaseFram):
    def __init__(self):
        super().__init__()
        Label(
            self,
            text="Tutorial",
            bg="red",
            fg="black",
            width="115",
            height="2",
            font=("Calibri", 100, "bold"),
        ).place(relx=0.51, rely=0.1, anchor=CENTER)
        Button(
            self,
            text="Go back",
            borderwidth=0,
            bg="yellow",
            height="2",
            width="30",
            font=("Calibri", 11, "bold"),
            command=lambda: show_frame(help),
        ).place(relx=0.01, rely=0.01, anchor=NW)
        Label(
            self,
            text="Draw a card from the pile if you can't play a card.",
            bg="yellow",
            height="5",
            width="60",
            font=("Calibri", 20, "bold"),
        ).place(relx=0.25, rely=0.5, anchor=CENTER)
        self.img = ImageTk.PhotoImage(Image.open("draw.png"))
        Label(self, image=self.img).place(relx=0.7, rely=0.5, anchor=CENTER)
        Button(
            self,
            text="Next",
            borderwidth=0,
            bg="yellow",
            height="2",
            width="30",
            font=("Calibri", 11, "bold"),
            command=lambda: show_frame(help3),
        ).place(relx=0.925, rely=0.975, anchor=S)


# ================Third Help window
class Help3(BaseFram):
    def __init__(self):
        super().__init__()
        Label(
            self,
            text="Tutorial",
            bg="red",
            fg="black",
            width="115",
            height="2",
            font=("Calibri", 100, "bold"),
        ).place(relx=0.51, rely=0.1, anchor=CENTER)
        Button(
            self,
            text="Go back",
            borderwidth=0,
            bg="yellow",
            height="2",
            width="30",
            font=("Calibri", 11, "bold"),
            command=lambda: show_frame(help2),
        ).place(relx=0.01, rely=0.01, anchor=NW)
        Label(
            self,
            text="Pay attention to action and wild cards.\n - A reverse card has two arrows going in opposite directions. It changes the direction of play. \n A skip card has a circle with a slash within it. It skips the player next to you. \n A draw two card has +2. It gives the next player 2 cards. \n A +4 card has +4 and is black. It can be placed on any card and gives the next player 4 cards.",
            bg="yellow",
            height="5",
            width="90",
            font=("Calibri", 20, "bold"),
        ).place(relx=0.5, rely=0.25, anchor=CENTER)
        self.img = ImageTk.PhotoImage(Image.open("card.png"))
        Label(self, image=self.img).place(relx=0.5, rely=0.7, anchor=CENTER)
        Button(
            self,
            text="Next",
            borderwidth=0,
            bg="yellow",
            height="2",
            width="30",
            font=("Calibri", 11, "bold"),
            command=lambda: show_frame(help4),
        ).place(relx=0.925, rely=0.975, anchor=S)


# =================Fourth Help window
class Help4(BaseFram):
    def __init__(self):
        super().__init__()
        Label(
            self,
            text="Tutorial",
            bg="red",
            fg="black",
            width="115",
            height="2",
            font=("Calibri", 100, "bold"),
        ).place(relx=0.51, rely=0.1, anchor=CENTER)
        Button(
            self,
            text="Go back",
            borderwidth=0,
            bg="yellow",
            height="2",
            width="30",
            font=("Calibri", 11, "bold"),
            command=lambda: show_frame(help3),
        ).place(relx=0.01, rely=0.01, anchor=NW)
        Label(
            self,
            text="Click -UNO- if you only have 1 card left. \n If you don't, you get +2 cards.",
            bg="yellow",
            height="5",
            width="60",
            font=("Calibri", 20, "bold"),
        ).place(relx=0.25, rely=0.5, anchor=CENTER)
        self.img = ImageTk.PhotoImage(Image.open("shout.png"))
        Label(self, image=self.img).place(relx=0.7, rely=0.5, anchor=CENTER)
        Button(
            self,
            text="Next",
            borderwidth=0,
            bg="yellow",
            height="2",
            width="30",
            font=("Calibri", 11, "bold"),
            command=lambda: show_frame(help5),
        ).place(relx=0.925, rely=0.975, anchor=S)


# ==================Fifth Heko window
class Help5(BaseFram):
    def __init__(self):
        super().__init__()
        Label(
            self,
            text="Tutorial",
            bg="red",
            fg="black",
            width="115",
            height="2",
            font=("Calibri", 100, "bold"),
        ).place(relx=0.51, rely=0.1, anchor=CENTER)
        Button(
            self,
            text="Go back",
            borderwidth=0,
            bg="yellow",
            height="2",
            width="30",
            font=("Calibri", 11, "bold"),
            command=lambda: show_frame(help4),
        ).place(relx=0.01, rely=0.01, anchor=NW)
        Label(
            self,
            text="Play your last card to win the hand.",
            bg="yellow",
            height="5",
            width="60",
            font=("Calibri", 20, "bold"),
        ).place(relx=0.25, rely=0.5, anchor=CENTER)
        self.img = ImageTk.PhotoImage(Image.open("win.png"))
        Label(self, image=self.img).place(relx=0.7, rely=0.5, anchor=CENTER)
        Button(
            self,
            text="Done",
            borderwidth=0,
            bg="yellow",
            height="2",
            width="30",
            font=("Calibri", 11, "bold"),
            command=lambda: show_frame(main_menu),
        ).place(relx=0.925, rely=0.975, anchor=S)


# ======================================================================================================================#


login = Login()
register = Register()
main_menu = MainMenu()
shop = Shop()
achievement = Achievements()
help = Help()
leaderboard = Leaderboard()
help2 = Help2()
help3 = Help3()
help4 = Help4()
help5 = Help5()

show_frame(login)


for frame in (
    login,
    register,
    main_menu,
    shop,
    achievement,
    help,
    leaderboard,
    help2,
    help3,
    help4,
    help5,
):
    frame.grid(row=0, column=0, sticky="nsew")

window.mainloop()

# ==================================
