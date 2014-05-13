import time

print("")

def createDefaultGrid():
    grid = [[0] * 9] * 9
    for i in range(9):
        grid[i] = [0,0,0,0,0,0,0,0,0]
    return grid

def createPopulatedGrid(sstr):
    grid = [[0] * 9] * 9
    for i in range(9):
        grid[i] = [int(sstr[0 * 9 + i]),int(sstr[1 * 9 + i]),int(sstr[2 * 9 + i]),int(sstr[3 * 9 + i]),int(sstr[4 * 9 + i]),int(sstr[5 * 9 + i]),int(sstr[6 * 9 + i]),int(sstr[7 * 9 + i]),int(sstr[8 * 9 + i])]
    return grid

def createSolutionsGrid():
    grid = [[[] * 9] * 9] * 9
    for i in range(9):
        grid[i] = [[],[],[],[],[],[],[],[],[]]
    return grid

def printGrid(grid):
    for x in range(9):
        row = " %s %s %s | %s %s %s | %s %s %s"
        for y in range(9):
            a = str(grid[y][x])
            if a == "0":
                a = "."
            row = row.replace("%s", a, 1)
        if x % 3 == 0 and x != 0:
            print("-------+-------+-------")
        print(row)

def isGridValid(grid):
    #Column valid
    for x in range(9):
        taken = [False] * 9
        for y in range(9):
            slot = grid[x][y]
            
            if slot != 0:
                if taken[slot - 1]:
                    return False
                taken[slot - 1] = True

    #Rows valid
    for x in range(9):
        taken = [False] * 9
        for y in range(9):
            slot = grid[y][x]
            if slot != 0:
                if taken[slot - 1]:
                    return False
                taken[slot - 1] = True

    #Box valid
    for gridX in range(3):
        for gridY in range(3):
            taken = [False] * 9
            for x in range(3):
                for y in range(3):
                    slot = grid[gridX * 3 + x][gridY * 3 + y]

                    if slot != 0:
                        if taken[slot - 1]:
                            return False
                        taken[slot - 1] = True
    return True

def isGridComplete(grid):
    for x in range(9):
        for y in range(9):
            if grid[x][y] == 0:
                return False
    return True

#Setting up arrays of arrays being the grid
grid = createPopulatedGrid("240315096108269704309000205010503080000000000700841002800070003000000000004000900")

for x in range(9):
    for y in range(9):
        pass
        #grid[x][y] = input("Please input " + str(x) + " " + str(y) + " slot")[0]
printGrid(grid)
print(isGridValid(grid))
print(isGridComplete(grid))

notSolved = True
start = time.clock()

while notSolved:
    solutions = createSolutionsGrid()

    hasSolutions = False
    
    for x in range(9):
        for y in range(9):
            if grid[x][y] != 0:
                continue
            for i in range(9):
                temp = grid[x][y]
                grid[x][y] = (i + 1)
                if isGridValid(grid):
                    solutions[x][y].append(i + 1)
                    hasSolutions = True
                grid[x][y] = temp

    doneForNow = False
    #First time check wheather only one number can fit
    for x in range(9):
        for y in range(9):
            if doneForNow:
                continue
            
            solution = solutions[x][y]
            if len(solution) == 1:
                grid[x][y] = solution[0]
            elif len(solution) > 1:
                for s in solution:
                    onlyCount = 0
                            
                    #Rows valid
                    for n in range(9):
                        for j in range(9):
                            slot = solutions[n][j]
                            if len(solutions[x][j]) == 0:
                                onlyCount += 9
                                break
                            elif slot != s:
                                onlyCount += 1
                            for gridX in range(3):
                                for gridY in range(3):
                                    bit = solutions[int(gridX * ((n - (n % 3)) / 3))][int(gridY * ((j - (j % 3)) / 3))]
                                    try:
                                        bit.index(s)
                                    except ValueError:
                                        onlyCount += 1
                    #Columns valid
                    for n in range(9):
                        for j in range(9):
                            slot = solutions[j][n]
                            if len(solutions[x][j]) == 0:
                                onlyCount += 9
                                break
                            elif slot != s:
                                onlyCount += 1
                            for gridX in range(3):
                                for gridY in range(3):
                                    bit = solutions[int(gridX * ((j - (j % 3)) / 3))][int(gridY * ((n - (n % 3)) / 3))]
                                    try:
                                        bit.index(s)
                                    except ValueError:
                                        onlyCount += 1
                    print(onlyCount)
                    if onlyCount >= 162:
                        grid[x][y] = s
                        doneForNow = True
                        break;

    if isGridComplete(grid) or not hasSolutions:
        notSolved = False

t = time.clock() - start
print("Time taken: " + str(round(t, 2)) + "s")
printGrid(grid)

    
