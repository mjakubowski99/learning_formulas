
def get_config_file_path_from_file_directory(path):
    config_path = path.split('/')[:-1]
    return "/".join(config_path) + "/" + "config.json"