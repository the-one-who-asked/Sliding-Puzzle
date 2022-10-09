from tkinter import *
from PIL import Image, ImageTk
import random
import numpy as np
import time


class MoveableButton(Button):
    def __init__(self, location, idx, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.location = location
        self.grid(column=location[0], row=location[1])
        self.idx = idx
        self.label = Label(root, text=idx)
        self.label.grid(column=self.location[0], row=self.location[1], sticky="nw")
        self.configure(command=self.line_move, width=100, height=100, borderwidth=0, highlightthickness=0)

    def move(self):
        global empty_square
        if any(abs(self.location[i] - empty_square[i]) == 1 and self.location[1-i] == empty_square[1-i] for i in range(2)):
            self.location, empty_square = empty_square, self.location
            self.grid(column=self.location[0], row=self.location[1])
            self.label.grid(column=self.location[0], row=self.location[1], sticky="nw")

    def line_move(self):
        global empty_square
        global pieces
        for i in range(2):
            loc, obj = self.location[1-i], empty_square[1-i]
            if self.location[i] == empty_square[i]:
                line_pieces = []
                for piece in pieces:
                    alt = piece.location[1-i]
                    if ((loc <= alt < obj) or (loc >= alt > obj)) and piece.location[i] == empty_square[i]:
                        line_pieces.append((piece, abs(obj-alt)))
                for piece in sorted(line_pieces, key=lambda x: x[1]):
                    piece[0].move()


def leftkey_pressed(event, shift=0):
    global empty_square
    global pieces
    global size
    for piece in pieces:
        loc, obj = piece.location, empty_square
        if loc[1] == obj[1]:
            if shift:
                pivot = obj[0]+shift if 0 <= obj[0]+shift < size else size-1
                if loc[0] == pivot:
                    piece.line_move()
                    break
            elif loc[0]-1 == obj[0]:
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
                pivot = obj[0]-shift if 0 <= obj[0]-shift < size else 0
                if loc[0] == pivot:
                    piece.line_move()
                    break
            elif loc[0]+1 == obj[0]:
                piece.move()
                break

def upkey_pressed(event, shift=0):
    global empty_square
    global pieces
    for piece in pieces:
        loc, obj = piece.location, empty_square
        if loc[0] == obj[0]:
            if shift:
                pivot = obj[1]+shift if 0 <= obj[1]+shift < size else size-1
                if loc[1] == pivot:
                    piece.line_move()
                    break
            elif loc[1]-1 == obj[1]:
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
                pivot = obj[1]-shift if 0 <= obj[1]-shift < size else 0
                if loc[1] == pivot:
                    piece.line_move()
                    break
            elif loc[1]+1 == obj[1]:
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
    shift = int(event.keysym)

def shuffle(event, events, size):
    global empty_square
    if event.keysym not in ("Shift_L", "Shift_R"):
        for i in range(5*size**3):
            event = events
            time.sleep(1/(5*size**3))
            if empty_square[0] > size/2: event.append(event[1])
            elif empty_square[0] < size/2: event.append(event[0])
            if empty_square[1] > size/2: event.append(event[3])
            elif empty_square[1] < size/2: event.append(event[2])
            random.choice(event)(1)
            root.update_idletasks()
        root.after(1000, check_completion)

def check_completion():
    global pieces
    global init_time
    global size
    if all(int(piece.idx)-1 == piece.location[1]*size + piece.location[0]  for piece in pieces):
        root.destroy()
        print(f"Congratulations! It took about: {time.strftime('%M:%S', time.gmtime(time.time()-init_time))}")
    root.after(1000, check_completion)


size = int(input("Enter a board size (3 - 7 are recommended): "))
root = Tk()
root.title("Sliding Puzzle")
empty_square = (size-1, size-1)
images = (
    "/Users/neerajarora/Downloads/sliding_puzzle_image1.webp",
    "/Users/neerajarora/Downloads/sliding_puzzle_image2.png",
    "/Users/neerajarora/Downloads/sliding_puzzle_image3.webp",
    "/Users/neerajarora/Downloads/sliding_puzzle_image4.jpeg",
    "/Users/neerajarora/Downloads/sliding_puzzle_image5.webp"
)
sliced_image = segment(Image.open(random.choice(images)), size)
button_images = [ImageTk.PhotoImage(image=Image.fromarray(sliced_image[i]).resize((100,100))) for i in range(size**2-1)]
init_time = time.time()
pieces = [MoveableButton((i%size, i//size), str(i+1), root, image=button_images[i]) for i in range(size**2-1)]
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
root.bind("<Key>", lambda x: shuffle(x, events, size))
root.mainloop()
