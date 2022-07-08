# shamelessly stolen from https://www.youtube.com/watch?v=I2lOwRiGNy4

import requests
from time import sleep
from threading import Thread
from Settings import *
from Sudoku import solve, find_empty
from PygameUtils import *

buffer = 5
secs = 0
mins = 0
hours = 0
running = True


def showTime():
    myFont = pygame.font.SysFont('Comic Sans MS', 30)
    global secs
    global mins
    global hours
    global win
    while running:
        secs += 1
        if secs % 60 == 0 and secs != 0:
            secs = 0
            mins += 1
        if mins % 60 == 0 and mins != 0:
            mins = 0
            hours += 1
        if secs < 10:
            secStr = f'0{str(secs)}'
        else:
            secStr = str(secs)
        if mins < 10:
            minStr = f'0{str(mins)}'
        else:
            minStr = str(mins)
        if hours < 10:
            hourStr = f'0{hours}'
        else:
            hourStr = str(hours)
        timeStr = f'{hourStr}:{minStr}:{secStr}'
        timeLabel = myFont.render(timeStr, True, CLOCKCOLOR)
        labelPos = (EDGE - timeLabel.get_width() - 25, EDGE - timeLabel.get_height() - 5)
        pygame.draw.rect(win, BACKGROUND,
                         (labelPos[0] - 10, labelPos[1], timeLabel.get_width() + 10, timeLabel.get_height()))
        win.blit(timeLabel, labelPos)
        pygame.display.update()
        sleep(1)


def insert(surface,grid_original,grid,solvedBoard, pos):
    i, j = pos[1], pos[0]
    global running
    global suceed
    while True:
        for event in pygame.event.get():
            pygame.draw.rect(surface, BLACK,
                             (pos[0] * 50 + buffer, pos[1] * 50 + buffer, 50 - 2 * buffer, 50 - 2 * buffer), 5)
            if event.type == pygame.QUIT:
                running = False

                return
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pygame.draw.rect(surface, BACKGROUND,
                                 (pos[0] * 50 + buffer, pos[1] * 50 + buffer, 50 - 2 * buffer, 50 - 2 * buffer), 5)
                fillGrid(win)
                pos = pygame.mouse.get_pos()
                pos = (pos[0] // 50, pos[1] // 50)
                i, j = pos[1], pos[0]
                pygame.draw.rect(surface, BLACK,
                                 (pos[0] * 50 + buffer, pos[1] * 50 + buffer, 50 - 2 * buffer, 50 - 2 * buffer), 5)
                continue
            if event.type == pygame.KEYDOWN:
                if grid_original[i - 1][j - 1] != 0:
                    return

                if event.key == 48 or event.key == 1073741922 or event.key == 127 or event.key == 8:  # checking with 0
                    grid[i - 1][j - 1] = event.key - 48
                    pygame.draw.rect(surface, BACKGROUND,
                                     (pos[0] * 50 + buffer, pos[1] * 50 + buffer, 50 - 2 * buffer, 50 - 2 * buffer))

                if 1 <= event.key - 48 < 10:
                    grid[i - 1][j - 1] = event.key - 48
                    pygame.draw.rect(surface, BACKGROUND,
                                     (pos[0] * 50 + buffer, pos[1] * 50 + buffer, 50 - 2 * buffer, 50 - 2 * buffer))

                if 1073741913 <= event.key < 1073741922:
                    pygame.draw.rect(surface, BACKGROUND,
                                     (pos[0] * 50 + buffer, pos[1] * 50 + buffer, 50 - 2 * buffer, 50 - 2 * buffer))
                    grid[i - 1][j - 1] = event.key - 1073741912
                pygame.display.update()
                if find_empty(grid) is None:
                    running = False
                    suceed = solvedBoard == grid
                return


def fillGrid(surface,grid_original,grid,solvedBoard):
    boldFont = pygame.font.SysFont('Comic Sans MS', 35, True)
    myFont = pygame.font.SysFont('Comic Sans MS', 35)
    value = myFont.render('', False, RED)
    for i in range(0, len(grid[0])):
        for j in range(0, len(grid[0])):
            if 0 < grid[i][j] < 10:
                if grid_original[i][j] != 0:
                    value = boldFont.render(str(grid[i][j]), False, original_grid_element_color)
                elif grid[i][j] == solvedBoard[i][j]:
                    value = myFont.render(str(grid[i][j]), False, GREY)
                elif grid[i][j] != solvedBoard[i][j]:
                    value = myFont.render(str(grid[i][j]), False, RED)
                surface.blit(value, ((j + 1) * 50 + 15, (i + 1) * 50))


def drawGrid():
    for i in range(0, 10):
        if i % 3 == 0:
            pygame.draw.line(win, FOREGROUND, (50 + 50 * i, 50), (50 + 50 * i, 500), 7)
            pygame.draw.line(win, FOREGROUND, (50, 50 + 50 * i), (500, 50 + 50 * i), 7)
        else:
            pygame.draw.line(win, FOREGROUND, (50 + 50 * i, 50), (50 + 50 * i, 500), 2)
            pygame.draw.line(win, FOREGROUND, (50, 50 + 50 * i), (500, 50 + 50 * i), 2)


def mainBtnClick():
    print('pressed')
    global runningMainMenu
    runningMainMenu = False
    difficultyMenu()
    return


def startGame(difficulty='easy'):
    global runningMainMenu
    runningMainMenu = False
    resp = requests.get(f'https://sugoku.herokuapp.com/board?difficulty={difficulty}')  # easy,medium,hard,random
    grid = resp.json()['board']
    solvedBoard = resp.json()['board']
    grid_original = [[grid[x][y] for y in range(len(grid[0]))] for x in range(len(grid))]
    solve(solvedBoard)

    main(grid,grid_original,solvedBoard)


def difficultyMenu():
    win.fill(actual_background)
    drawGrid()
    btnEasy = Button(win, (EDGE // 2) - 100, 125, 200, text='easy')
    btnEasy.color = GREEN
    btnEasy.hoverColor = (0, 200, 0)
    btnEasy.font.color = BLACK
    btnEasy.font.hoverColor = WHITE
    btnEasy.onClick = startGame
    while True:
        btnEasy.draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()


def mainMenu():
    win.fill(actual_background)
    drawGrid()
    btnStart = Button(win, (EDGE // 2) - 100, 125, 200, text='Start Game')
    btnStart.color = GREEN
    btnStart.hoverColor = (0, 200, 0)
    btnStart.font.color = BLACK
    btnStart.font.hoverColor = WHITE
    btnStart.onClick = mainBtnClick
    while runningMainMenu:
        btnStart.draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()


def main(grid,grid_original,solvedBoard):
    global running
    pygame.display.set_caption('Sudoku')
    win.fill(BACKGROUND)
    t = Thread(target=showTime)
    t.start()
    myFont = pygame.font.SysFont('Comic Sans MS', 35, True)
    drawGrid()
    for i in range(0, len(grid[0])):
        for j in range(0, len(grid[0])):
            if 0 < grid[i][j] < 10:
                value = myFont.render(str(grid[i][j]), True, original_grid_element_color)
                win.blit(value, ((j + 1) * 50 + 15, (i + 1) * 50))
    pygame.display.update()
    while running:
        fillGrid(win,grid_original,grid,solvedBoard)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                insert(win,grid_original,grid,solvedBoard, (pos[0] // 50, pos[1] // 50))
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                return


def blink(window):
    blinking = True
    global actual_background
    while blinking:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                blinking = False
                pygame.quit()
        if actual_background == BACKGROUND:
            if suceed:
                pygame.draw.rect(window, GREEN, (0, 0, EDGE, EDGE), 50)
                actual_background = GREEN
            else:
                pygame.draw.rect(window, RED, (0, 0, EDGE, EDGE), 50)
                actual_background = RED
        else:
            pygame.draw.rect(window, BACKGROUND, (0, 0, EDGE, EDGE), 50)
            actual_background = BACKGROUND
        pygame.display.update()
        sleep(1)


if __name__ == '__main__':
    suceed = None
    actual_background = BACKGROUND
    pygame.init()
    win = pygame.display.set_mode((EDGE, EDGE))
    runningMainMenu = True
    mainMenu()
    # main()
    blink(win)
