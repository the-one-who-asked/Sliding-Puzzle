from tkinter import *
import random
import numpy as np
import threading

def main(size):
    global final_log
    global threads
    grid = np.array(range(1, size**2+1), dtype="uint32").reshape(size, size)
    grid[-1][-1] = 0
    original_grid = np.copy(grid)
    log = []

    def l(grid):
        pos = np.array([int(np.where(grid == 0)[i]) for i in range(2)])
        grid[pos[0]][pos[1]], grid[pos[0]][pos[1]+1] = grid[pos[0]][pos[1]+1], 0
        return grid
    def r(grid):
        pos = np.array([int(np.where(grid == 0)[i]) for i in range(2)])
        grid[pos[0]][pos[1]], grid[pos[0]][pos[1]-1] = grid[pos[0]][pos[1]-1], 0
        return grid
    def d(grid):
        pos = np.array([int(np.where(grid == 0)[i]) for i in range(2)])
        grid[pos[0]][pos[1]], grid[pos[0]+1][pos[1]] = grid[pos[0]+1][pos[1]], 0
        return grid
    def u(grid):
        pos = np.array([int(np.where(grid == 0)[i]) for i in range(2)])
        grid[pos[0]][pos[1]], grid[pos[0]-1][pos[1]] = grid[pos[0]-1][pos[1]], 0
        return grid

    choices = [l, r, u, d]
    pos = np.array([int(np.where(grid == 0)[i]) for i in range(2)])
    if pos[0] == size - 1:
        choices.remove(l)
    elif pos[0] == 0:
        choices.remove(r)
    if pos[1] == size - 1:
        choices.remove(d)
    elif pos[1] == 0:
        choices.remove(u)
    for i in range(5*size**3):
        grid = random.choice(choices)(grid)


    def process(size, grid, log, original_grid):
        print("processing")
        global event
        global final_log
        global threads
        global lock
        while not event.is_set():
            print("starting loop")
            if np.all(grid == original_grid):
                print(grid)
                final_log = log
                event.set()
                break
            choices = [l, r, u, d]
            pos = np.array([int(np.where(grid == 0)[i]) for i in range(2)])
            if log:
                if log[-1] == "r":
                    if l in choices: choices.remove(l)
                elif log[-1] == "l":
                    if r in choices: choices.remove(r)
                elif log[-1] == "d":
                    if u in choices: choices.remove(u)
                elif log[-1] == "u":
                    if d in choices: choices.remove(d)
            if pos[1] == size - 1:
                if l in choices: choices.remove(l)
            elif pos[1] == 0:
                if r in choices: choices.remove(r)
            if pos[0] == size - 1:
                if u in choices: choices.remove(u)
            elif pos[0] == 0:
                if d in choices: choices.remove(d)

            break_p = [choice.__name__ for choice in choices]

            for choice in choices[1:]:
                child = threading.Thread(target=process, args=(size, choice(grid), log+[choice.__name__], original_grid))
                threads.append(child)
                child.start()
            grid = choices[0](grid)
            log.append(choices[0].__name__)
            with lock:
                print(log)


    process(5, grid, log, original_grid)
    for thread in threads:
        thread.join()
    print(final_log, grid)

if __name__ == "__main__":
    event = threading.Event()
    final_log = []
    lock = threading.RLock()
    threads = []
    main(5)