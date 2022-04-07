import shlex
import subprocess
import os
from pathlib import Path

INSTANCE = "instance_4"

def run(children, strategy, memOffset, reductionThreshold, localCostFunc):
    epos = """### Dataset ###
#The folder name in the datasets path. Make sure it has no spaces, tabs or newlines (alphanum and underscore preferred)
dataset=energy


### Basic epos properties ###
# any integer > 0
numSimulations=50

# any integer > 0
numIterations=50

# any integer > 0
numAgents=1000

# any integer > 0
numPlans=10

# any integer > 0
numChildren={}

# exact dimensionality from the dataset
planDim=144


### Shuffle seeds ###

# initial agent structure before reorganization occurs, any integer > 0
shuffle=0

# path to a file containing permutation of indices, need its strucure: sphinx one column: integer index in each row
shuffle_file="permutation.csv"


### Multi-objective Cost Weights ###
# Number of supported objectives: 3
# Efficiency objective: 1-alpha-beta
# Fairness objective: alpha
# Discomfort objective: beta
# (1-alpha-beta)*inefficiency + alpha*unfairness + beta*discomfort
# "alpha,beta", e.g. "0.3,0.7" for alpha=0.3 and beta=0.7
# this needs to be removed actually
numberOfWeights = 2
# Weights are in string format, separated by ","
weightsString = "0.0,0.0"


### Reorganization strategy ###

# possible values: periodically, convergence, globalCostReduction, never. never_strategy: never does reorganization
strategy={}

# any integer > 0, if "periodically" strategy is chosen
periodically.reorganizationPeriod=5

# any positive integer (>0), if "convergence" strategy is chosen, the iteration at which the selections will be memorized to be sued after the following reorganization
convergence.memorizationOffset={}

# double from [0, 1]
globalCost.reductionThreshold={}

# any integer. Keep the same seed to reproduce experiment results, what random permutations each strategy will explore, result reproducability
strategy.reorganizationSeed=0



#sphinx
#vector target for global response same dimensionality as plan
#filepath
goalSignalPath=default

# Values: "VAR", "RSS", "XCORR", "RMSE"
# Goal signal is ignored in functions with only global response as input, e.g. var
globalCostFunction=VAR

# Values: "STD", "UNIT-LENGTH", "MIN-MAX" (only for RSS).
scaling="MIN-MAX"

# Values: "INDEX", "DISC", "PREF"
localCostFunction="{}"


### Loggers ###
logger.GlobalCostLogger = true
logger.LocalCostMultiObjectiveLogger = false
logger.TerminationLogger = false
logger.SelectedPlanLogger = false
logger.GlobalResponseVectorLogger = false
logger.PlanFrequencyLogger = false
logger.UnfairnessLogger = false
logger.GlobalComplexCostLogger = false
logger.WeightsLogger = false
logger.ReorganizationLogger = false
logger.VisualizerLogger = false

#Code related logger for debugging and checks
# please check here https://docs.oracle.com/javase/7/docs/api/java/util/logging/Level.html. For experiments "SEVERE" is preferred
logLevel="SEVERE"
""".format(children, strategy, memOffset, reductionThreshold, localCostFunc )

    with open(r'{}/conf/epos.properties'.format(INSTANCE), "w") as myfile:
        myfile.write(epos)
        myfile.close()

    cd = os.getcwd()
    inst_path = os.path.join(cd, r'{}'.format(INSTANCE))

    os.chdir(r"{}".format(inst_path))

    cdd = os.path.join(cd, r'{}/conf'.format(INSTANCE))
    fdd = os.path.join(cd, r'{}//EPOS-Tutorial.jar'.format(INSTANCE))
    cdd = r"/home/big-data/bigdata/Python/{}/conf".format(INSTANCE)


    command = r'java -jar "{}" "{}"'.format(fdd, cdd)
    process = subprocess.Popen(shlex.split(command))
    process.wait()

    os.chdir("..")


lcfs = ["DISC", "PREF", "INDEX"]
strats = ["convergence", "globalCostReduction"]

# 1560 runs
for l in range(0, 3):
    lcf = lcfs[l]
    for s in range(0, 2):
        strat = strats[s]
        for i in range(1, 21):
            memOff = i
            globCostThresh = i/20
            for c in range(1, 14):
                childs = c
                run(childs, strat, memOff, globCostThresh, lcf)
