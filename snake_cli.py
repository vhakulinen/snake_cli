import curses
import time
from threading import Thread
import random

#field will be in format of [y,x]
#Field properties
FIELD_WIDTH = 40
FIELD_HEIGHT = 25
#field it self
field = [ ]

#snake { block : [x,y,moving_state] } ex. snake[2][0] to
#get x cordinate from block 2 and snake[2][1]
#to get y cordinate from block 2 and snake[2][2]
#to get direction from block 2, direction=
#1=right 2=left 3=up 4=down

snake = { 0 : [ 3, 6, 2 ],
          1 : [ 4, 6, 2 ],
          2 : [ 5, 6, 2 ],
          3 : [ 6, 6, 2 ],
        }

#lets print this before we initialize curses so that if it fails
#user will know what to do. it actually doesn't fail here if it fails, it fails
#when we try draw stuff and we dont have big enough window.
print "Make sure you have huge enough window!"
#curses stuffz
stdscr = curses.initscr()
curses.noecho()
curses.cbreak()

#global variables
inputKey = 0 #<--- in ascii
gameRunning = True
#food [x,y,is_alive] is_alive; 0 = true 1 = false
food = [ 2, 2, 1 ]
score = 0
dead = False

#another thread for getting "keyboard state"
def thread_input():
    global inputKey
    while gameRunning:
        #get input
        inputKey = stdscr.getch()
        #sleep
        time.sleep(0.3)
        #set input to null
        inputKey = 0

def draw():
    #Draw field
    for y in range(len(field)):
        for x in range(len(field[y])):
            if field[y][x] == "0":
                stdscr.addch(y + 1, x + 1, " ")
            else:
                stdscr.addch(y + 1, x + 1, field[y][x])

    #information
    stdscr.addstr(3, FIELD_WIDTH + 10, "Score: %s" % score)
    stdscr.refresh()

def process():
    global snake
    global food
    global gameRunning
    global score

    #process snake
    for block in range(len(snake)):
        if block is not 0:
            snake[block - 1][2] = snake[block][2]
        #if direction is left (1)
        if snake[block][2] == 1:
            #if direction is opposet
            if snake[block][2] == 2:
                snake[block][2] = 4
            #can we move ?
            if snake[block][0] - 1 < 0:
                #if not, move it to another side of field
                snake[block][0] = FIELD_WIDTH - 1
            else:
                #if we can, lets move it
                snake[block][0] -= 1
        #if direction is right (2)
        if snake[block][2] == 2:
            if snake[block][0] + 2 > FIELD_WIDTH:
                snake[block][0] = 0
            else:
                snake[block][0] += 1
        #if direction is up (3)
        if snake[block][2] == 3:
            if snake[block][1] - 1 < 0:
                snake[block][1] = FIELD_HEIGHT -1 
            else:
                snake[block][1] -= 1
        #if direction is down (4)
        if snake[block][2] == 4:
            if snake[block][1] + 2 > FIELD_HEIGHT:
                snake[block][1] = 0
            else:
                snake[block][1] += 1

    #if snake ate foodz
    if snake[len(snake) - 1][0] == food[0]:
        if snake[len(snake) - 1][1] == food[1]:
            #lets set food to dead
            food[2] = 1
            #score
            score += 1
            #lets move all snake's block one forward
            for block in range(len(snake)-1, -1, -1):
                snake[block + 1] = snake[block]
            #and now we can and one block to the tail
            tmpDirect = 1
            tmpX = 1
            tmpY = 1
            if snake[1][2] == 1:
                tmpDirect = 2
                tmpX = snake[1][0] - 1
                tmpY = snake[1][1]
            if snake[1][2] == 2:
                tmpDirect = 1
                tmpX = snake[1][0] + 1
                tmpY = snake[1][1]
            if snake[1][2] == 3:
                tmpDirect = 4
                tmpX = snake[1][0]
                tmpY = snake[1][1] - 1
            if snake[1][2] == 4:
                tmpDirect = 3
                tmpX = snake[1][0]
                tmpY = snake[1][1] + 1
            snake[0] = [tmpX, tmpY, tmpDirect]

    #genFood if not alive
    if food[2] == 1:
        while food[2] is not 0:
            food = genFood()

    #empty the field
    for y in range(FIELD_HEIGHT):
        for x in range(FIELD_WIDTH):
            field[y][x] = "0"
    #add the snake to field
    for block in range(len(snake)):
        x = snake[block][0]
        y = snake[block][1]
        if field[y][x] == "x" and block is len(snake) - 1:
            gameRunning = False
        else:
            field[y][x] = "x"
    #add food to field
    field[food[1]][food[0]] = "*"

    time.sleep(0.3)

def Input():
    global gameRunning
    if chr(inputKey) == "q":
        gameRunning = False
    

    #change direction; if it is opposed as where we are going atm, do change it to closest one
    if chr(inputKey) == "a":
        if snake[len(snake) - 1][2] == 2:
            snake[len(snake) - 1][2] = 4
        else:
            snake[len(snake) - 1][2] = 1
    if chr(inputKey) == "d":
        if snake[len(snake) - 1][2] == 1:
            snake[len(snake) - 1][2] = 3
        else:
            snake[len(snake) - 1][2] = 2
    if chr(inputKey) == "w":
        if snake[len(snake) - 1][2] == 4:
            snake[len(snake) - 1][2] = 1
        else:
            snake[len(snake) - 1][2] = 3
    if chr(inputKey) == "s":
        if snake[len(snake) - 1][2] == 3:
            snake[len(snake) - 1][2] = 2
        else:
            snake[len(snake) - 1][2] = 4

def genFood():
    randOK = True
    x = random.randrange(0, FIELD_WIDTH)
    y = random.randrange(0, FIELD_HEIGHT)
    for block in range(len(snake)):
        if snake[block][0] is not x and snake[block][1] is not y:
            pass
        else:
            randOK = False
    if randOK:
        return [x, y, 0]
    else:
        return [x, y, 1]


"""
INITIALIZE SECTION
"""

#loop trough height
for y in range(FIELD_HEIGHT):
    #add list in to list to be y cordinate
    field.append([])
    #loop trough width
    for x in range(FIELD_WIDTH):
        #add int to list to be x cordinate
        field[y].append("0")

#add snake to the field
for block in range(len(snake)):
    x = snake[block][0]
    y = snake[block][1]
    field[y][x] = "x"

#Draw borders
#First and last row
for i in range(FIELD_WIDTH + 2):
    stdscr.addch(0, i, "-")
    stdscr.addch(FIELD_HEIGHT + 1, i, "-")
#Everything in between first and last row
for i in range(FIELD_HEIGHT + 1):
    stdscr.addch(i, 0, "-")
    stdscr.addch(i, FIELD_WIDTH + 1, "-")

#Add some information to the screen
stdscr.addstr(5, FIELD_WIDTH + 10, "Use WASD to move.")
stdscr.addstr(6, FIELD_WIDTH + 10, "You can press 'q' anytime to quit.")

while food[2] is not 0:
    food = genFood()

#MAIN
if __name__ == "__main__":
    inputThread = Thread(target=thread_input)
    inputThread.start()

    while gameRunning:
        if dead:
            gameOver()
        Input()
        process()
        draw()

    curses.echo()
    curses.endwin()

    print "\nYour score was %d. Gz!\n" % score

    print "Waiting for input thread to stop."
    #wait for threads to stop
    inputThread.join()
    print "Bye."
