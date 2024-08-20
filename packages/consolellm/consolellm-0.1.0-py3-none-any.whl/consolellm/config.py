from os import getenv
import os
import toml

def create_config():
    curr_dir = os.getcwd()
    print(f"Current working directory: {curr_dir}")
    config_path = curr_dir+"/.config/config.toml"

    if not os.path.exists(curr_dir+"/.config"):
        os.makedirs(curr_dir+"/.config")

        api_key = input("Open Router API key: ")
        sys_prompt = input("System Prompt (blank for default): ")
        config_data = {
            "api_key": api_key,
            "system_prompt": sys_prompt if sys_prompt else "You are the greatest coder on earth, you can solve any coding question correctly in one go. Always give the output in markdown format. You are a great coding assistant."
        }

        with open(config_path, "w") as config_file:
            toml.dump(config_data, config_file)
        print("Configuration saved successfully.")

        with open(config_path, "r") as config_file:
            config_data = toml.load(config_file)

        api_key = config_data.get("api_key")
        system_prompt = config_data.get("system_prompt")

        return api_key, system_prompt

    else:
        with open(config_path, "r") as config_file:
            config_data = toml.load(config_file)

        api_key = config_data.get("api_key")
        system_prompt = config_data.get("system_prompt")

        print("Configuration loaded successfully")

        return api_key, system_prompt