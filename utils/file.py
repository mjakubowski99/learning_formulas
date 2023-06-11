import os 

def get_config_file_path_from_file_directory(path):
    config_path = path.split('/')[:-1]
    return "/".join(config_path) + "/" + "config.json"

def get_file_real_dir(file):
    path = os.path.realpath(file)
    
    index = path.rfind('/')
    if index == -1:
        raise Exception("Invalid path")
    
    return path[:index]
    

    
