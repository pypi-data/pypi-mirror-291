def get_config_yaml(config_path):
    # read the file inferless.yaml in the current directory as a json string
    try:
        with open(config_path, "r") as file:
            config_yaml = file.read()
            return config_yaml
    except FileNotFoundError:
        raise Exception("Configuration file inferless.yaml not found in the current directory")
    except Exception as e:
        raise Exception(f"Error reading inferless.yaml file: {e}")
