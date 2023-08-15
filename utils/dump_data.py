import os
import shutil
import argparse
from file import *

parser = argparse.ArgumentParser()
parser.add_argument('--copy-data', action='store_true')
args, leftovers = parser.parse_known_args()

copy_data_files = False 
if hasattr(args, 'copy_data') and args.copy_data:
    copy_data_files = True 

project_dir = get_file_real_dir(__file__ + "/..")
train_file = project_dir+'/core/data/train.txt'
test_file = project_dir+'/core/data/test.txt'
result_file = project_dir+'/core/result/result.txt'
datasets_dir = project_dir+'/datasets'
dumps_dir = project_dir+"/dumps"

if not os.path.exists(dumps_dir):
    os.makedirs(dumps_dir)

dump_name = input("Podaj nazwę dumpa: ")
dataset_dir_name = input('Podaj katalog datasetu w folderze datasets: ')

config_file_path = datasets_dir+"/"+dataset_dir_name+"/config.json"

dumps_dir = dumps_dir+"/"+dump_name
if not os.path.exists(dumps_dir):
    os.makedirs(dumps_dir)

if copy_data_files:
    shutil.copy(config_file_path, dumps_dir+"/config.json")
    shutil.copy(train_file, dumps_dir+"/train.txt")
    shutil.copy(test_file, dumps_dir+"/test.txt")

shutil.copy(result_file, dumps_dir+"/result.txt")



