import numpy as np
import numexpr as ne
import random
import matplotlib.pyplot as mtplt
import seaborn as sns

numRandVars = int(input("number of randomized variables: "))   #User input number of ranomdized vars
numSetVars = int(input("number of set variables: "))           #User input number of set variables
numSimulatedTime = int(input("Number of unit time per simulation: "))
numSimulations = int(input("Number of simulations to be run (the more, the more statistically accurate, but longer loading time): "))

randVars = {}       #Randomized variables and their lower and upper bounds
setVars = {}        #Set variables and their set values
allVars = {}        #All variables, including randomized variables after their randomized value is determined

def replace_all(text, dic):
    for i, j in dic.items():
        text = text.replace(i, j)
    return text

def uniformRandomize(randomVarArray):
    randomizedVarsArr = {}
    for key in randomVarArray:
        min = randomVarArray.get(key)[0]
        max = randomVarArray.get(key)[1]
        fixed = random.uniform(min,max)
        randomizedVarsArr.update({key:fixed})

    return randomizedVarsArr

def combineDicts(dict1,dict2):
    combinedDict = {}

    combinedDict.update(dict1)
    combinedDict.update(dict2)

    return combinedDict


def equationCalc(equationStr, variableDict):                        #Equivalent of the "simulated day" method in original MC sim
    return ne.evaluate(equationStr, global_dict = variableDict)

def unitSimulation(equationStr, randomVarDict, setVarDict , simulatedTime):       #Equivalent of "storage unit profit"
    valueTotal = 0
    valueArray = []
    valueArray.append(0)

    for x in range(simulatedTime):
        fullVarDict = combineDicts(setVars, uniformRandomize(randVars))

        valueTotal += equationCalc(equationStr,fullVarDict)
        valueArray.append(valueTotal)

    # print (valueArray)
    return valueArray

#The following is only necessary in the standalone code--when the frontend just sends dictionaries, this wont be necessary anymore:

for n in range(numRandVars):                                                                                                                                        #Input for all randomized variables, based on the number of variables user specified
    rangeArray = []
    newRandKey = input("Enter Your Randomized Variable Name (#" + str(n+1) + "): ")
    rangeArray.append(float(input(str(newRandKey) + " Lower Bound: ")))
    rangeArray.append(float(input(str(newRandKey) + " Upper Bound: ")))
    randVars[newRandKey]= rangeArray

for n in range(numSetVars):                                                                                                                                         #Input for all set variables, based on the number of variables user specified
    newSetKey = input("Enter Your Set Variable Name (#" + str(n+1) + "): ")
    setVars[newSetKey] = float(input((str(newSetKey) + " Set Value: ")))

#end of placeholder code

equation = input("Input your expression in terms of the inputted variables (Please place all non-algebraic functions in parantheses, Ex sin(x+y), or exp(3*d+p): ") #input must be expression
functionReplacements = {"sin": "numpy.sin", "cos": "numpy.cos", "tan": "numpy.tan", "log": "numpy.log", "exp": "numpy.exp"}                                              #need to include documentation for how to use certain functions (like log)
newEquation = replace_all(equation, functionReplacements)

timeArray = []
timeArray.append(0)
for time in range(numSimulatedTime):
    timeArray.append(time)


allSims = []
for sims in range(numSimulations):
    allSims.append(unitSimulation(equation,randVars,setVars,numSimulatedTime))

finalProfits = []
for simulation in range(len(allSims)):
    finalProfits.append(allSims[simulation][numSimulatedTime - 1])

print (finalProfits)

for sim in range(numSimulations):
    mtplt.plot(timeArray, allSims[sim])

mtplt.xlabel('Time (days)')
mtplt.ylabel('Profit ($)')
mtplt.draw()

mtplt.figure()
sns.distplot(finalProfits, hist=False, kde=True, label='Probability Density')
mtplt.xlabel('Profit ($)')
mtplt.ylabel('Probability Density')
mtplt.draw()

mtplt.show()

#where we are right now: trying to convert input expression into an expression that sympy can interpret.
#  need to find a way to input values from dictionaries into sympy values