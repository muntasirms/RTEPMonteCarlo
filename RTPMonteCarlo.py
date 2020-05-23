# each line represents a single unit
# each point of a line is a simulated day with randomized parameters
# we are looking to see each percentile's profit after a given amount of simulated days of multiple simulated units
# this is a tool for powell--so keep things easy to change--variables at the top and clearly labeled, code commented and understandable
# model lithium ion and thermal as you guys found--maybe find a more competitive efficiency for thermal online
# you can use peak and trough pricing as a generalized model--but how can you simulate changes in price?

import random
import numpy as np
import matplotlib.pyplot as mtplt
import seaborn as sns
from flask import Flask, request
app = Flask(__name__)

# maxPeakPrice = .11  # Maximum peak price ($/kWh)
# minPeakPrice = .0672  # Minimum peak price ($/kWh)
#
# maxTroughPrice = .0751  # Maximum trough price ($/kWh)
# minTroughPrice = .05  # Minimum trough price ($/kWh)
#
# maxStorageTime = 5  # Maximum amount of time energy will be stored for
# minStorageTime = 3  # Minimum amount of time energy will be stored for
#
# isThermal = True  # If thermal storage is being modeled, set to True. For all other technologies, set to False
# capacity = 2500  # Storage capacity--amount of energy required to charge storage unit (kWh)
# efficiency = .41  # Conversion efficiency of unit (0-1)
# efficiencyLoss = .00037  # Proportion of total storage lost per hour
# heatRecycling = .54  # Thermal only, proportion of lost heat recycled (0-1)
#
# simulatedDays = 3650  # The number of simulated days each unit will undergo
# numSimulations = 1000  # Number of units to be simulated. The more units, the more statistically accurate results


def simulatedDay(maxPeakPrice, minPeakPrice, maxTroughPrice, minTroughPrice, maxStorageTime, minStorageTime,
                 isThermal, capacity, efficiency, efficiencyLoss, heatRecycling):
    simPeakPrice = random.uniform(minPeakPrice, maxPeakPrice)
    simTroughPrice = random.uniform(minTroughPrice, maxTroughPrice)
    simStorageTime = random.uniform(minStorageTime, maxStorageTime)

    storageLoss = simStorageTime * efficiencyLoss * capacity
    chargeCost = simTroughPrice * capacity
    dischargeCost = simPeakPrice * efficiency * (capacity - storageLoss)

    if isThermal:
        heatRecycleProfit = (1 - efficiency) * capacity * heatRecycling * simPeakPrice
        profit = dischargeCost - chargeCost + heatRecycleProfit

        # print(simPeakPrice,simTroughPrice)
        return profit

    else:
        profit = dischargeCost - chargeCost

        return profit


def storageUnitProfit(maxPeakPrice, minPeakPrice, maxTroughPrice, minTroughPrice, maxStorageTime, minStorageTime,
                 isThermal, capacity, efficiency, efficiencyLoss, heatRecycling, simDays):
    profitArray = []
    profitTotal = 0

    for x in range(simDays):
        profitTotal += simulatedDay(maxPeakPrice, minPeakPrice, maxTroughPrice, minTroughPrice, maxStorageTime, minStorageTime,
                                    isThermal, capacity, efficiency, efficiencyLoss, heatRecycling)
        profitArray.append(profitTotal)

    return profitArray


@app.route('/getChart', methods=['GET'])
def getChart():
    maxPeakPrice = float(request.args.get('maxPeakPrice'))  # Maximum peak price ($/kWh)
    minPeakPrice = float(request.args.get('minPeakPrice'))  # Minimum peak price ($/kWh)

    maxTroughPrice = float(request.args.get('maxTroughPrice'))  # Maximum trough price ($/kWh)
    minTroughPrice = float(request.args.get('minTroughPrice'))  # Minimum trough price ($/kWh)

    maxStorageTime = float(request.args.get('maxStorageTime'))  # Maximum amount of time energy will be stored for
    minStorageTime = float(request.args.get('minStorageTime'))  # Minimum amount of time energy will be stored for

    isThermal = True if request.args.get('isThermal')=="True" else False # If thermal storage is being modeled, set to True. For all other technologies, set to False
    capacity = float(request.args.get('capacity'))  # Storage capacity--amount of energy required to charge storage unit (kWh)
    efficiency = float(request.args.get('efficiency'))  # Conversion efficiency of unit (0-1)
    efficiencyLoss = float(request.args.get('efficiencyLoss'))  # Proportion of total storage lost per hour
    heatRecycling = float(request.args.get('heatRecycling'))  # Thermal only, proportion of lost heat recycled (0-1)

    simulatedDays = int(request.args.get('simulatedDays'))  # The number of simulated days each unit will undergo
    numSimulations = int(request.args.get('numSimulations'))  # Number of units to be simulated. The more units, the more statistically accurate results

    dayArray = []

    for days in range(simulatedDays):
        dayArray.append(days)

    allUnits = []
    for sims in range(numSimulations):
        allUnits.append(storageUnitProfit(maxPeakPrice, minPeakPrice, maxTroughPrice, minTroughPrice, maxStorageTime, minStorageTime,
                 isThermal, capacity, efficiency, efficiencyLoss, heatRecycling, simulatedDays))

    for sim in range(numSimulations):
        mtplt.plot(dayArray, allUnits[sim])

    finalProfits = []

    for simulation in range(len(allUnits)):
        finalProfits.append(allUnits[simulation][simulatedDays - 1])
        # print(allUnits[simulation][simulatedDays-1])

    ninetyPercentile = np.percentile(finalProfits, 90)
    tenPercentile = np.percentile(finalProfits, 10)
    median = np.median(finalProfits)

    print('Median: $' + str(round(median, 2)))
    print('90th Percentile: $' + str(round(ninetyPercentile, 2)))
    print('10th Percentile: $' + str(round(tenPercentile, 2)))

    if isThermal:
        mtplt.title('Monte Carlo Simulation of TES @' + str(efficiency * 100) + '% Efficiency, and ' + str(
            heatRecycling * 100) + '% Heat Recycling')
    else:
        mtplt.title('Monte Carlo Simulation of Energy Storage @' + str(efficiency * 100) + '% Efficiency')

    mtplt.xlabel('Time (days)')
    mtplt.ylabel('Profit ($)')
    mtplt.draw()

    mtplt.figure()
    if isThermal:
        mtplt.title('Probability Density of TES Profits@' + str(efficiency * 100) + '% Efficiency, and ' + str(
            heatRecycling * 100) + '% Heat Recycling')
    else:
        mtplt.title('Probability Density of Energy Storage Profits @' + str(efficiency * 100) + '% Efficiency')

    sns.distplot(finalProfits, hist=False, kde=True, label='Probability Density')

    mtplt.xlabel('Profit ($)')
    mtplt.ylabel('Probability Density')

    mtplt.draw()

    mtplt.show()
    return "done"


if __name__ == '__main__':
    app.run()
