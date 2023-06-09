
def get_config_file_for_dataset(path):
    config_path = path.split('/')[:-1]
    return "/".join(config_path) + "/" + "config.json"