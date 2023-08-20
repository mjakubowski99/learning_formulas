from sklearn.model_selection import ParameterGrid
import subprocess
import sys

tries = 3

grid = {
    "ALGORITHM": ["EVOLUTION"],
    "TRAIN_FILE_NAME": ["../data/train.txt"],
    "TEST_FILE_NAME": ["../data/test.txt"],
    "RESULT_DIR": ["../result/"],
    "MIN_CLAUSES_COUNT": [10],
    "MAX_CLAUSES_COUNT": [10],
    "MIN_LITERALS_COUNT": [2],
    "MAX_LITERALS_COUNT": [2],
    "POPULATIONS_COUNT": [5,10,15,20,25,30,35,40],
    "POPULATIONS_SIZE": [100],
    "FINAL_POPULATION_SIZE": [100],
    "NEW_FORMULAS_PERCENTAGE": [1],
    "CROSSING_PERCENTAGE": [0]
}

parameters_combinations = list(ParameterGrid(grid))

def run(cmd):
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE)

    while process.stdout.readable():
        line = process.stdout.readline()

        if not line:
            break

        print(line.strip())


def write_to_env(params):
    with open(".env", "w") as f:
        for variable in params:
            f.write(variable+"="+str(params[variable])+'\n')
    f.close()

for params in parameters_combinations:
    if params["MIN_CLAUSES_COUNT"] != params["MAX_CLAUSES_COUNT"]:
        continue
    if params["MIN_LITERALS_COUNT"] != params["MAX_LITERALS_COUNT"]:
        continue

    write_to_env(params)

    for i in range(0,tries):
        run("./run.sh")