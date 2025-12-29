import curses
import random
import time

WIDTH, HEIGHT = 15, 40

SHAPES = [
    [(0,0),(1,0),(0,1),(1,1)],          # O
    [(0,0),(1,0),(2,0),(3,0)],          # I
    [(0,0),(1,0),(2,0),(1,1)],          # T
    [(0,0),(0,1),(1,1),(2,1)],          # L
    [(2,0),(0,1),(1,1),(2,1)],          # J
]

def rotate(shape):
    return [(-y, x) for x, y in shape]

def collision(board, shape, ox, oy):
    for x, y in shape:
        nx, ny = x + ox, y + oy
        if nx < 0 or nx >= WIDTH or ny >= HEIGHT:
            return True
        if ny >= 0 and board[ny][nx]:
            return True
    return False

def clear_lines(board):
    board[:] = [row for row in board if any(c == 0 for c in row)]
    while len(board) < HEIGHT:
        board.insert(0, [0]*WIDTH)

def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(1)
    board = [[0]*WIDTH for _ in range(HEIGHT)]

    shape = random.choice(SHAPES)
    x, y = WIDTH//2, -1

    while True:
        stdscr.clear()

                # ----- SHOW CONTROLS (PRINT STATEMENTS IN CURSES WAY) -----
        stdscr.addstr(1, WIDTH*2 + 3, "Controls:")
        stdscr.addstr(3, WIDTH*2 + 3, "A- Left")
        stdscr.addstr(4, WIDTH*2 + 3, "D - Right")
        stdscr.addstr(5, WIDTH*2 + 3, "S - Down")
        stdscr.addstr(6, WIDTH*2 + 3, "W - Rotate")
        stdscr.addstr(7, WIDTH*2 + 3, "Q - Quit")

        key = stdscr.getch()
        if key == ord('q'):
            break
        if key == ord('a') and not collision(board, shape, x-1, y):
            x -= 1
        if key == ord('d') and not collision(board, shape, x+1, y):
            x += 1
        if key == ord('s') and not collision(board, shape, x, y+1):
            y += 1
        if key == ord('w'):
            r = rotate(shape)
            if not collision(board, r, x, y):
                shape = r

        if not collision(board, shape, x, y+1):
            y += 1
        else:
            for bx, by in shape:
                board[y+by][x+bx] = 1
            clear_lines(board)
            shape = random.choice(SHAPES)
            x, y = WIDTH//2, -1
            if collision(board, shape, x, y):
                break

        for i in range(HEIGHT):
            for j in range(WIDTH):
                if board[i][j]:
                    stdscr.addstr(i, j*2, "[]")

        for bx, by in shape:
            if y+by >= 0:
                stdscr.addstr(y+by, (x+bx)*2, "[]")

        stdscr.refresh()
        time.sleep(0.20)

curses.wrapper(main)
