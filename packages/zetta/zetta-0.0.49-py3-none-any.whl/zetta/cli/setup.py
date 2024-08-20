# Copyright ZettaBlock Labs 2024
import os
import io
import pyfiglet
import requests
import configparser
import webbrowser
from zetta._utils.async_utils import synchronizer

SERVICE_SIGNIN_URL = "https://stage-app.zettablock.dev/aiweb/tokens"
SERVICE_GET_USER_URL = "https://neo-dev.prod.zettablock.com/v1/api/user"
HEADERS = {
    "Authorization": ""
}

@synchronizer.create_blocking
async def setup():
    try:
        block_text = pyfiglet.figlet_format("ZETTA", font="block")
        block_text = block_text.rstrip()
        print(f"{block_text}\n")
        zetta_root = os.path.expanduser("~")
        zetta_dir = setup_zettadir(zetta_root)
        token = get_token_from_file(zetta_dir)
        profile_data = None
        if token is not None:
            profile_data = get_user_profile(token)
        if token is None or profile_data is None:
            webbrowser.open(SERVICE_SIGNIN_URL)
            token = input("To finish the setup, `zetta` requires a token generated from https://stage-app.zettablock.dev/aiweb/tokens: ")
            profile_data = get_user_profile(token)
        generate_profile_file(zetta_dir, profile_data)
        print_directory_structure(zetta_dir)
    except Exception as e:
        print(f"An error occurred: {e}")
    pass


def get_token_from_file(zetta_dir):
    file_path = os.path.join(zetta_dir, "secrets")
    if not os.path.exists(file_path) or not os.path.isfile(file_path):
        return None
    config = configparser.ConfigParser()
    config.read(file_path)
    token = config.get('default', 'token')
    if token is None or token == "":
        return None
    return token


def get_user_profile(token):
    HEADERS['Authorization'] = token
    response = requests.get(SERVICE_GET_USER_URL, headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    else:
        return None


def existed(d, key):
    if d[key] != "" and d[key] is not None:
        return True
    return False


def generate_profile_file(zetta_dir, profile_data, profile_name="default"):
    config = configparser.ConfigParser()
    config[profile_name] = {}
    if existed(profile_data["data"]["profile"], "tokens"):
        for token in profile_data["data"]["profile"]["tokens"]:
            if token.get("is_default"):
                config[profile_name]["token"] = token["id"]
                break
    if existed(profile_data["data"]["profile"], "api_keys"):
        for api_key in profile_data["data"]["profile"]["api_keys"]:
            if api_key.get("is_default"):
                config[profile_name]["api_key"] = api_key["id"]
                break
    if existed(profile_data["data"]["profile"], "wallet_address"):
        config[profile_name]["wallet_address"] = profile_data["data"]["profile"]["wallet_address"]
    if existed(profile_data["data"]["profile"], "hf_token"):
        config[profile_name]["hf_token"] = profile_data["data"]["profile"]["hf_token"]
    file_path = os.path.join(zetta_dir, "secrets")
    with io.StringIO() as config_string:
        config.write(config_string)
        content = config_string.getvalue()
        content = content.rstrip('\n')
    with open(file_path, "w") as configfile:
        configfile.write(content)

    config.clear()
    config[profile_name] = {}
    if existed(profile_data["data"]["user"], "tenant"):
        config[profile_name]["tenant"] = profile_data["data"]["user"]["tenant"]
    if existed(profile_data["data"]["user"], "user_name"):
        config[profile_name]["user_name"] = profile_data["data"]["user"]["user_name"]
    if existed(profile_data["data"]["user"], "email"):
        config[profile_name]["email"] = profile_data["data"]["user"]["email"]
    file_path = os.path.join(zetta_dir, "profile")
    with io.StringIO() as config_string:
        config.write(config_string)
        content = config_string.getvalue()
        content = content.rstrip('\n')
    with open(file_path, "w") as configfile:
        configfile.write(content)


def print_directory_structure(root_dir):
    for root, dirs, files in os.walk(root_dir):
        level = root.replace(root_dir, '').count(os.sep)
        indent = '│   ' * level + '├── ' if level > 0 else ''
        if os.path.basename(root) == ".zetta":
            print(f"{indent}{root}/")
        else:
            print(f"{indent}{os.path.basename(root)}/")
        sub_indent = '│   ' * (level + 1) + '├── '
        for f in files:
            print(f"{sub_indent}{f}")


def setup_zettadir(zetta_root):
    zetta_dir = os.path.join(zetta_root, ".zetta")
    if not os.path.exists(zetta_dir):
        os.makedirs(zetta_dir)
    return zetta_dir
