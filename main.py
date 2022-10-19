from tkinter import *
from PIL import Image, ImageTk
import random
import numpy as np
import time
from ctypes import windll


class MoveableButton(Button):
    def __init__(self, location, idx, img, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.location = location
        self.grid(column=location[0], row=location[1], sticky="news")
        self.idx = idx
        self.img = img
        self.searched = False
        self.label = Label(board, text=idx, bg="#333333", fg="#FFFFFF")
        self.label.grid(column=self.location[0], row=self.location[1], sticky="nw")
        self.image = ImageTk.PhotoImage(image=self.img)
        self.configure(command=self.line_move, image=self.image, bd=0, highlightthickness=0)

    def move(self):
        global empty_square
        global moves
        if any(abs(self.location[i] - empty_square[i]) == 1 and self.location[1 - i] == empty_square[1 - i] for i in
               range(2)):
            self.location, empty_square = empty_square, self.location
            self.grid(column=self.location[0], row=self.location[1])
            self.label.grid(column=self.location[0], row=self.location[1], sticky="nw")
            moves += 1

    def line_move(self):
        global empty_square
        global pieces
        for i in range(2):
            loc, obj = self.location[1 - i], empty_square[1 - i]
            if self.location[i] == empty_square[i]:
                line_pieces = []
                for piece in pieces:
                    alt = piece.location[1 - i]
                    if ((loc <= alt < obj) or (loc >= alt > obj)) and piece.location[i] == empty_square[i]:
                        line_pieces.append((piece, abs(obj - alt)))
                for piece in sorted(line_pieces, key=lambda x: x[1]):
                    piece[0].move()

    def search(self):
        global search_var
        searched_id = search_var.get()
        if self.idx == searched_id and int(self.idx) - 1 == self.location[1] * size + self.location[0]:
            self.label.configure(bg="#357a38")
            self.searched = True
        elif self.idx == searched_id:
            self.label.configure(bg="#e1ad01", fg="#333333")
            self.searched = True
        elif searched_id == str(self.location[1] * size + self.location[0] + 1):
            self.label.configure(bg="#ff6600")
            self.searched = True
        elif self.searched:
            self.label.configure(bg="#333333", fg="#FFFFFF")
            self.searched = False
        root.after(1000, self.search)


    def expand(self):
        global size
        width = board.winfo_width() // size
        height = root.winfo_height() // size
        self.image = ImageTk.PhotoImage(image=self.img.resize((width, height)))
        self.configure(image=self.image)
        root.after(1000, self.expand)


def leftkey_pressed(event, shift=0):
    global empty_square
    global pieces
    global size
    for piece in pieces:
        loc, obj = piece.location, empty_square
        if loc[1] == obj[1]:
            if shift:
                pivot = obj[0] + shift if 0 <= obj[0] + shift < size else size - 1
                if loc[0] == pivot:
                    piece.line_move()
                    break
            elif loc[0] - 1 == obj[0]:
                piece.move()
                break

def rightkey_pressed(event, shift=0):
    global empty_square
    global pieces
    global size
    for piece in pieces:
        loc, obj = piece.location, empty_square
        if loc[1] == obj[1]:
            if shift:
                pivot = obj[0] - shift if 0 <= obj[0] - shift < size else 0
                if loc[0] == pivot:
                    piece.line_move()
                    break
            elif loc[0] + 1 == obj[0]:
                piece.move()
                break

def upkey_pressed(event, shift=0):
    global empty_square
    global pieces
    for piece in pieces:
        loc, obj = piece.location, empty_square
        if loc[0] == obj[0]:
            if shift:
                pivot = obj[1] + shift if 0 <= obj[1] + shift < size else size - 1
                if loc[1] == pivot:
                    piece.line_move()
                    break
            elif loc[1] - 1 == obj[1]:
                piece.move()
                break

def downkey_pressed(event, shift=0):
    global empty_square
    global pieces
    global size
    for piece in pieces:
        loc, obj = piece.location, empty_square
        if loc[0] == obj[0]:
            if shift:
                pivot = obj[1] - shift if 0 <= obj[1] - shift < size else 0
                if loc[1] == pivot:
                    piece.line_move()
                    break
            elif loc[1] + 1 == obj[1]:
                piece.move()
                break


def segment(image, segments):
    image = np.array(image)
    cropping = image.shape[0] // segments * segments
    image = image[:cropping, :cropping]
    s = [image.shape[0] * i // segments for i in range(segments + 1)]
    return [image[s[j]:m, s[i]:n] for j, m in enumerate(s[1:]) for i, n in enumerate(s[1:])]


def shift_control(event):
    global shift
    global size
    global search_var
    global search_entry
    if event.keysym != search_var.get()[-1] or search_entry["state"] == "disabled":
        shift = int(event.keysym) if int(event.keysym) else size - 1

def shuffle(event, events, size):
    global empty_square
    global init_time
    global moves
    if event.keysym not in ("Shift_L", "Shift_R", "BackSpace"):
        for i in range(5 * size ** 3):
            event = events
            time.sleep(1 / (5 * size ** 3))
            if empty_square[0] > size / 2:
                event.append(event[1])
            elif empty_square[0] < size / 2:
                event.append(event[0])
            if empty_square[1] > size / 2:
                event.append(event[3])
            elif empty_square[1] < size / 2:
                event.append(event[2])
            random.choice(event)(1)
            root.update_idletasks()
        root.after(1000, check_completion)
        init_time = time.time()
        moves = 0
        root.after(1000, update)


def update():
    global timer
    global init_time
    global moves
    timer.configure(text=f"time taken: {time.strftime('%M:%S', time.gmtime(time.time() - init_time))}\nmoves: {moves}")
    root.after(1000, update)

def check_completion():
    global pieces
    global init_time
    global moves
    global size
    if all(int(piece.idx)-1 == piece.location[1]*size + piece.location[0] for piece in pieces):
        root.destroy()
        print(f"Congratulations! It took about: {time.strftime('%M:%S', time.gmtime(time.time() - init_time))} minutes and {moves} moves")
    root.after(1000, check_completion)


size = int(input("Enter a board size (3 - 7 are recommended): "))
windll.shcore.SetProcessDpiAwareness(1)
init_time = 0
moves = 0

root = Tk()
root.title(f"({size}x{size}) - {size**2 - 1} Puzzle")
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.rowconfigure(0, weight=1)
length = (3*root.winfo_screenheight()) // (4*size)
board = Frame(root, width=length*size, height=length*size, bd=0, bg="#333333")
board.grid(row=0, column=0, sticky="news")
stats = Frame(root, width=length, height=length*size, bd=0, bg="#444444")
stats.grid(row=0, column=1, sticky="news")
search_box = Frame(stats, bd=2, bg="#444444")
search_box.grid(row=1, column=0, ipadx=2, ipady=2, sticky="news")
search_box.columnconfigure(0, weight=1)
search_box.columnconfigure(1, weight=3)
for i in range(size):
    board.rowconfigure(i, weight=1)
    board.columnconfigure(i, weight=1)
for i in range(11):
    stats.rowconfigure(i, weight=1, minsize=(length*size)//11)

empty_square = (size - 1, size - 1)
images = (
    "https://github.com/the-one-who-asked/Sliding-Puzzle/blob/63bb7ae485e91dec4981badddc04be4196a1e3d6/images/sliding_puzzle_image1.webp",
    "https://github.com/the-one-who-asked/Sliding-Puzzle/blob/63bb7ae485e91dec4981badddc04be4196a1e3d6/images/sliding_puzzle_image1.webp",
    "https://github.com/the-one-who-asked/Sliding-Puzzle/blob/63bb7ae485e91dec4981badddc04be4196a1e3d6/images/sliding_puzzle_image1.webp",
    "https://github.com/the-one-who-asked/Sliding-Puzzle/blob/63bb7ae485e91dec4981badddc04be4196a1e3d6/images/sliding_puzzle_image1.webp",
    "https://github.com/the-one-who-asked/Sliding-Puzzle/blob/63bb7ae485e91dec4981badddc04be4196a1e3d6/images/sliding_puzzle_image1.webp",
    "https://github.com/the-one-who-asked/Sliding-Puzzle/blob/63bb7ae485e91dec4981badddc04be4196a1e3d6/images/sliding_puzzle_image1.webp",
    "https://github.com/the-one-who-asked/Sliding-Puzzle/blob/63bb7ae485e91dec4981badddc04be4196a1e3d6/images/sliding_puzzle_image1.webp"
)
sliced_image = segment(Image.open(random.choice(images)), size)
button_images = [Image.fromarray(sliced_image[i]).resize((length,length)) for i in range(size**2-1)]
pieces = [MoveableButton((i%size, i//size), str(i+1), button_images[i], board) for i in range(size**2-1)]
for piece in pieces:
    root.after(1000, piece.expand)

timer = Label(stats, text="time taken: 00:00\nmoves: 0", bd=0, bg="#e1ad01", fg="#444444", width=18, justify="left")
timer.grid(row=0, column=0, ipadx=1, ipady=1, sticky="nw")
claim = Label(stats, text="Made by Ansh Arora", bd=0, bg="#444444", fg="#e1ad01")
claim.grid(row=10, column=0, sticky="s")

icon_image = ImageTk.PhotoImage(image=Image.open(r"C:\Users\AnshArora\Downloads\search_icon.png").resize((25, 25)))
search_icon = Label(search_box, image=icon_image, bg="#444444", bd=2, width=25)
search_icon.grid(column=0, row=0, sticky="news")
search_var = StringVar()
search_entry = Entry(search_box, textvariable=search_var, bg="#333333", fg="#FFFFFF", bd=2, width=12)
search_entry.grid(column=1, row=0, sticky="news")
search_entry.bind("<Leave>", lambda x: search_entry.configure(state="disabled"))
search_entry.bind("<Enter>", lambda x: search_entry.configure(state="normal"))
for piece in pieces:
    root.after(1000, piece.search)

events = [leftkey_pressed, rightkey_pressed, upkey_pressed, downkey_pressed]
shift = size
for i in range(10):
    root.bind(str(i), shift_control)
root.bind("<Left>", events[0])
root.bind("<Right>", events[1])
root.bind("<Up>", events[2])
root.bind("<Down>", events[3])
root.bind("<Shift-Left>", lambda x: leftkey_pressed(0, shift))
root.bind("<Shift-Right>", lambda x: rightkey_pressed(0, shift))
root.bind("<Shift-Up>", lambda x: upkey_pressed(0, shift))
root.bind("<Shift-Down>", lambda x: downkey_pressed(0, shift))
root.bind("a", events[0])
root.bind("d", events[1])
root.bind("w", events[2])
root.bind("s", events[3])
root.bind("<A>", lambda x: leftkey_pressed(0, shift))
root.bind("<D>", lambda x: rightkey_pressed(0, shift))
root.bind("<W>", lambda x: upkey_pressed(0, shift))
root.bind("<S>", lambda x: downkey_pressed(0, shift))
root.bind("<Key>", lambda x: shuffle(x, events, size))

root.mainloop()
