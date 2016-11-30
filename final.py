#
##
###
####
#    Andrew Meehan & Julien Chien
####
###
##
#

#   PROGRAM: Picobot Genetic Algorithm
#   GOAL: 1) Simulate the picobot environment. Randomly produce 200 picobot
#            programs with their own commands (gen 1)
#         2) Pick the fittest programs from the previous generation and put them
#            in the next generation. Then
#            mate and mutate programs to fill up the next generation.
#         3) Repeat until it is generation 20, where hopefully many programs can
#            traverse the square picobot maze

import random

HEIGHT = 25
WIDTH = 25
NUMSTATES = 5

STEPS = 2250
TRIALS = 50

class Program:
    def __init__(self):

        self.rules = {}
        self.randomize()


    def __repr__(self):
        keylist = self.rules.keys()
        keylist.sort()

        s = ""
        for each_key in range(len(keylist)):
            s += str(keylist[each_key][0])
            s +=" "
            s += str(keylist[each_key][1])
            s += " -> "
            s += str(self.rules[keylist[each_key]][0])
            s += ' '
            s += str(self.rules[keylist[each_key]][1])
            s += "\n"
        return s

    def randomize(self):
        """generates a random full set of rules for the self.rules dictionary!
        """
        possible_surroundings = ['xxxx', 'Nxxx', 'NExx', 'NxWx', 'xxxS', 'xExS',
                                 'xxWS', 'xExx', 'xxWx']
        movedirections = ['N', 'E', 'W', 'S']
        possible_states = range(NUMSTATES)

        for each_state in range(len(possible_states)):

            for each_surrounding in range(len(possible_surroundings)):

                movedir = random.choice(movedirections)
                while movedir in possible_surroundings[each_surrounding]:
                    movedir = random.choice(movedirections)

                movestate = random.choice(possible_states)
                self.rules[(possible_states[each_state],
                  possible_surroundings[each_surrounding])] =
                       (movedir, movestate)

    def getMove(self, state, surroundings):
        """get move takes and integerstate and a surrounding and returns a tuple
           that contains the picobot's next move and new state
        """
        ans = self.rules[(state, surroundings)]
        return ans


    def mutate(self):
        """mutates a single rule and state in the dictionary
        """
        possible_surroundings = ['xxxx', 'Nxxx', 'NExx', 'NxWx', 'xxxS', 'xExS',
                                 'xxWS', 'xExx', 'xxWx']

        movedirections = ['N', 'E', 'W', 'S']
        currState = random.choice(range(5))
        mSurr = random.choice(possible_surroundings)
        mState = random.choice(range(5))
        mDir = random.choice(movedirections)
        while mDir in mSurr:
            mDir = random.choice(movedirections)

        self.rules[(currState, mSurr)] = (mDir, mState)

        return self

    def crossover(self,other):
        """crosses the rules from 2 different programs using a random choice
           takes all moves below and at the random state choice and adds them
           to a new dictionary

           then takes all moves above the random state choice and adds moves
           from the 2nd program to the new dictionary sets self.rules as the new
           dictionary
        """
        #finds the highest state to takerules from p1
        topstate = random.choice(range(1,4))
        newrules = {}    #empty new rule dictionary
        keys1 = self.rules.keys()   #gets list of keys from self.rules
        keys1.sort()   #sorts list
        keys2 = other.rules.keys()   #same but for other program
        keys2.sort()     #sorts

        for eachkey in range(len(keys1)):
            if keys1[eachkey][0] <= topstate:
                newrules[keys1[eachkey]] = self.rules[(keys1[eachkey])]

        for eachkey in range(len(keys2)):
            if keys2[eachkey][0] > topstate:
                newrules[keys2[eachkey]] = other.rules[(keys2[eachkey])]

        crossProg = Program()
        crossProg.rules = newrules
        return crossProg

class World:
    def __init__(self, initial_row, initial_col, program):
        self.prow = initial_row
        self.pcol = initial_col
        self.numstates = NUMSTATES
        self.height = HEIGHT
        self.width = WIDTH
        self.state = 0
        self.prog = program
        self.room = [ [' ']*WIDTH for row in range(HEIGHT)]
        self.room[self.prow][self.pcol] = 'P'

    def __repr__(self):
        """
        returns the picobot board
        """

        s = ''   # the string to return
        s += '\n'
        s += '+'
        s += '-' * (self.width+2)
        s += '+'
        s += '\n'
        for row in range( self.height ):
            s += '| '

            for col in range( self.width ):
                s += self.room[row][col]
            s += ' |\n'

        s += '+'
        s += '-'*(self.width+2)    # add the bottom of the board
        s += '+'
        s += '\n'

        s += '\n'
        return s      # the board is complete, return it

    def getCurrentSurroundings(self):

        """returns a string in the NExx format as corresponds to the bot's
           current surroundings
        """

        csstring = ''

        if self.prow == 0:
            csstring += 'N'
        else:
            csstring += 'x'

        if self.pcol == 24 or self.pcol == -1:
            csstring += 'E'
        else:
            csstring += 'x'

        if self.pcol == 0:
            csstring += 'W'
        else:
            csstring += 'x'

        if self.prow == 24 or self.prow == -1:
            csstring += 'S'
        else:
            csstring += 'x'

        return csstring

    def step(self):

        currCol = self.pcol
        currRow = self.prow

        self.room[currRow][currCol] = 'o'
        movetodo = self.prog.getMove(self.state, self.getCurrentSurroundings())

        if movetodo[0] == 'E' and 'E' not in self.getCurrentSurroundings():
            self.pcol = self.pcol + 1
        elif movetodo[0] == 'W' and 'W' not in self.getCurrentSurroundings():
            self.pcol = self.pcol - 1
        elif movetodo[0] == 'N' and 'N' not in self.getCurrentSurroundings():
            self.prow = self.prow - 1
        elif movetodo[0] == 'S' and 'S' not in self.getCurrentSurroundings():
            self.prow = self.prow + 1

        self.room[self.prow][self.pcol] = 'P'
        self.state = movetodo[1]

    def run(self, steps):
        for x in range(steps):
            self.step()

    def run2(self, steps):
        stepCounter = 0
        for x in range(steps):
            self.step()
            stepCounter += 1
            if stepCounter == (steps/2):
                if self.repeatChecker() == True:
                    if steps % 2 == 1:
                        self.step()
                        return
                    else:
                        return
                elif self.repeatChecker() == False and steps > 1:
                    steps = steps - 2

    def fractionVisitedCells(self):
        """returns a float point fraction of cells in self.room that are marked
           'o'/'P'
        """
        x=0
        for row in range(self.height):
            for col in range(self.width):
                if self.room[row][col] == 'o' or self.room[row][col] == 'P':
                    x += 1
        y = 25**2
        z = (x*1.0)/(y*1.0)
        return z

    def repeatChecker(self):
        """This function is built to speed up the fitness testing so
           picobot doesn't waste computer run time repeating abitrary steps in
           an unfit program
        """

        stateatMoment = self.state
        fracCells = self.fractionVisitedCells
        nextMove = self.getCurrentSurroundings()

        self.step()
        self.step()

        state2 = self.state
        fracCellsNow = self.fractionVisitedCells
        move2 = self.getCurrentSurroundings()

        if stateatMoment == state2 and fracCells == fracCellsNow and nextMove == move2:

            return True
        else:
            return False

def evaluateFitness(program, TRIALS, STEPS):
    p = program
    fitList = []
    dirtyList = []
    for each_trial in range(TRIALS):
        w = World(random.choice(range(25)),random.choice(range(25)),p)
        w.run(STEPS)
        cellsCovered = w.fractionVisitedCells()
        dirtyList.append(cellsCovered)
    fitness = ((sum(dirtyList) * 1.0) / (TRIALS*1.0))
    fitness = "%8.4f" % fitness
    fitness = float(fitness)
    return fitness

def menu(numProgs, Generations):
    s = ''

    s += '\n\n\n'
    s += '_-_-_-_-' * 3
    s += ' W E L C O M E '
    s += '-_-_-_-_' * 3
    s += '\n\n\n'
    s += '      You have initialized the Genetic Algorithm program'
    s += '\n'
    s += '       There will be '
    s += str(numProgs)
    s += ' programs per generation.'
    s += '\n\n'
    s += '         There will be '
    s += str(Generations)
    s += ' generations.'
    s += '\n'
    s += '\n'
    s += '            Fitness is measured using 50 random trials per program'
    s += '\n'
    s += '      (therefore 50 random starting postions, unless randoms are duplicated)'
    s += '\n'
    s += '                         Each trial runs 3000 steps'
    s += '\n'
    s += '\n'

    return s

def GA(numProgramsperGen, Generations):
    s = menu(numProgramsperGen, Generations)
    print s

    dictionary = genProgs(numProgramsperGen)
    picoRules = dictionary.values()
    programNames = dictionary.keys()
    picoRules.sort()
    programNames.sort()

    GenerationCounter = 1
    while GenerationCounter != (Generations+1):

        fitEvaluated = []

        for eachProgram in programNames:
            name = eachProgram
            rules = dictionary[name]
            fitness = evaluateFitness(rules, TRIALS, 3000)
            x = (fitness, name, rules)
            fitEvaluated.append(x)

        fitEvaluated.sort()

        maxFitness = max(fitEvaluated)[0]

        SumFitness = 0
        for eachTuple in fitEvaluated:
            SumFitness += eachTuple[0]
        avgFitness = (SumFitness*1.0)/(len(fitEvaluated))
        bestRules = max(fitEvaluated)[2]
        bestProg = max(fitEvaluated)[1]
        fitAvg = avgFitness
        fitAvg = "%8.4f" % fitAvg
        print '\n'
        print '            GENERATION ' + str(GenerationCounter)
        print '\n'
        print 'The AVERAGE FITNESS for GENERATION ' + str(GenerationCounter) + ' is ' + str(fitAvg)
        print '\n'
        print 'The MAX FITNESS for GENERATION ' + str(GenerationCounter) + ' is ' + str(maxFitness)
        if maxFitness > 0.92:
            print '\n'
            print 'Wow! What a fit program!'
            print '\n'
            print 'Here\'s the picobot code for it!'
            print '\n'
            print bestRules
        print '\n'
        print 'Best program is:     ' + bestProg
        print '------------------------------------'
        print '\n'
        print '\n'

        fitAvg = float(fitAvg)

        dictionary = reproduce3(fitEvaluated, fitAvg, dictionary, maxFitness)
        programNames = dictionary.keys()
        picoRules = dictionary.values()
        picoRules.sort()
        programNames.sort()
        print 'Got the new dict'

        GenerationCounter += 1

        if GenerationCounter == (Generations + 1):
            print '\n'
            fitList = []
            maxfitness = fitEvaluated[-1][0]
            for eachProg in picoRules:
                fitness = evaluateFitness(eachProg,50,2500)
                if fitness >= maxfitness:
                    maxfitness = fitness
                    maxrules = eachProg
            for fitness in fitEvaluated:
                fitList.append(fitness[0])
            totFit = sum(fitList)
            avgFinal = (totFit*1.0) / (numProgramsperGen * 1.0)

            print 'The most fit program is: ' + str(fitEvaluated[-1][1]) + ' with a fitness of ' + str(maxfitness)
            print '\n'
            print 'The rules used by the most fit program are as follows: '
            print '\n'
            print str(fitEvaluated[-1][2])
            print '\n'
            print '\n'
            print 'The average fitness for your genetic algorthim is: ' + str(avgFinal)
            print '\n'
            print '\n'

            choice = raw_input('Would you like to run the program again?? (y/n): ')
            if choice.lower() == 'n' or choice.lower() == 'no':
                return
            else:
                numProgs = input('How many programs would you like to run per generation??: ')
                numGens = input('How many generations would you like to produce?: ')
                GA(numProgs,numGens)

def reproduce3(fitEvaluated, avgFit, dictionary, maxFit):
    fitEvaluated.sort()

    dictToReturn = {}

    goodProgs = []
    listOfNames = []
    for eachTuple in fitEvaluated:
        listOfNames.append(eachTuple[1])
        if eachTuple[0] > (((maxFit + avgFit)*1.0)/2.0):
            dictToReturn[eachTuple[1]]=eachTuple[2]
            goodProgs.append(eachTuple[1])

    while len(dictToReturn) != len(dictionary):
        goodProg = dictionary[random.choice(goodProgs)]
        randomTuple = random.choice(fitEvaluated)
        randomProg = randomTuple[2]
        progToAdd = goodProg.crossover(randomProg)

        if len(dictToReturn) % 15 == 0:
            print 'Mutate!'
            progToAdd.mutate()

        progName = str(genName(dictToReturn))
        dictToReturn[progName] = progToAdd

    if len(dictToReturn) == len(dictionary):
        return dictToReturn

def genName(dictionary):
    names = dictionary.keys()
    names.sort()
    #print names
    newName = names[-1]
    newName = str(newName[0:-1]) + str(int(newName[-1])+1)
    counter = len(dictionary)
    while newName in names:
        newName = 'prog'+str(counter+1)
        counter += 1
    return newName

def createNewGen(genList, aveFit):
    """creates a new generation using the most fit programs from the previous
       generation
    """
    d = {}

    counter = 0

    for eachprog in range(len(genList)):
        if genList[eachprog][0] >= aveFit:
            d[genList[eachprog][1]]

def genProgs(number_of_programs):
    """this creates and names x number of programs
    """

    d = {}

    counter = 0

    for eachprog in range(number_of_programs):
        d[('prog' + str(counter))] = Program()
        counter += 1

    return d

def fitAverage(L):
    """takes a list of fitnesses and program names and returns the average
       fitness
    """

    tot = 0
    for eachscore in range(len(L)):
        tot += L[eachscore][0]

    avg = (tot*1.0)/len(L)
    return avg

