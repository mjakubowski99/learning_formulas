from sklearn.model_selection import ParameterGrid
import subprocess
import sys

algorithm = "EVOLUTION"
result_dir = "../result/"
train_file_name = "../data/train.txt"
test_file_name = "../data/test.txt"

min_clauses_count = [3,4,5]
max_clauses_count = [5,6,7]
min_literals_count = [3,4,5]
max_literals_count = [5,6,7]
populations_count = [20,30,40,50,60,70,80]
population_size = [100]
final_population_size = [100]
new_formulas_percentage = [1]

tries = 5

grid = {
    "ALGORITHM": ["EVOLUTION"],
    "TRAIN_FILE_NAME": ["../data/train.txt"],
    "TEST_FILE_NAME": ["../data/test.txt"],
    "RESULT_DIR": ["../result/"],
    "MIN_CLAUSES_COUNT": [3,4,5],
    "MAX_CLAUSES_COUNT": [5,6,7],
    "MIN_LITERALS_COUNT": [3,4,5],
    "MAX_LITERALS_COUNT": [5,6,7],
    "POPULATIONS_COUNT": [20,30,40,50,60,70,80],
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
    with open("../.env", "w") as f:
        for variable in params:
            f.write(variable+"="+str(params[variable])+'\n')
    f.close()

for params in parameters_combinations:
    if params["MIN_CLAUSES_COUNT"] > params["MAX_CLAUSES_COUNT"]:
        continue
    if params["MIN_LITERALS_COUNT"] > params["MAX_LITERALS_COUNT"]:
        continue

    write_to_env(params)

    for i in range(0,tries):
        run("./../run.sh")