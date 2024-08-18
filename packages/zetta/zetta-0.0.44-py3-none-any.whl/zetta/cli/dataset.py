# Copyright ZettaBlock Labs 2024
import configparser
import os
import requests
import typer
from zetta._utils.async_utils import synchronizer

dataset_cli = typer.Typer(
    name="dataset",
    help="Manage your datasets in Zetta AI Network.",
    no_args_is_help=True,
)

SERVICE_CREATE_DATASET_URL = "https://neo-dev.prod.zettablock.com/v1/api/asset"
SERVICE_GITEA_URL = "https://gitea.stag-vxzy.zettablock.com"

@dataset_cli.command(name="create", help="create a new dataset repo.")
@synchronizer.create_blocking
async def create(dataset_name: str = typer.Argument(..., help="Name of the dataset"),
                    description: str = typer.Argument(..., help="Description of the dataset"),
                    license_type: str = typer.Argument(..., help="License type of the dataset"),
                    modality_type: str = typer.Argument(..., help="Modality of the dataset. E.g text, image, etc"),
                    private: bool = typer.Argument(..., help="Is the dataset private or not")):
    zetta_root = os.getenv("ZETTA_ROOT")

    if not zetta_root:
        raise EnvironmentError("ZETTA_ROOT env variable is not set.")
    secrets_path = os.path.join(zetta_root, ".zetta/secrets")

    try:
        config = configparser.ConfigParser()
        config.read(secrets_path)
        token = config.get('default', 'token', fallback=None)
    except FileNotFoundError:
        print(f"File not found: {secrets_path}")
    except IOError:
        print(f"An error occurred while reading the file: {secrets_path}")

    headers = {
        "Authorization": token
    }

    json_data = {
        "type": "Dataset",
        "name": dataset_name,
        "license": license_type,
        "description": description,
        "private": private,
        "modality": modality_type
    }

    response = requests.post(SERVICE_CREATE_DATASET_URL, headers=headers, json=json_data)
    if response.status_code == 200:
        print(f'Successfully created dataset {dataset_name}')
    else:
        response.raise_for_status()



@dataset_cli.command(name="delete", help="delete a dataset repo")
@synchronizer.create_blocking
async def delete(json: bool = False):
    pass


@dataset_cli.command(name="ownership", help="list dataset ownership.")
@synchronizer.create_blocking
async def ownership(json: bool = False):
    pass


@dataset_cli.command(
    name="lineage", help="list the lineage (with rewards info) for the dataset."
)
@synchronizer.create_blocking
async def lineage(json: bool = False):
    pass


@dataset_cli.command(name="logs", help="list the access logs for the dataset.")
@synchronizer.create_blocking
async def logs(json: bool = False):
    pass


@dataset_cli.command(name="history", help="list the git history for the dataset.")
@synchronizer.create_blocking
async def history(dataset_name: str = typer.Option(..., help="Name of the dataset"),
                    num_commits: int = typer.Option(10, help="Number of commits to display")):
    zetta_root = os.getenv("ZETTA_ROOT")

    if not zetta_root:
        raise EnvironmentError("ZETTA_ROOT env variable is not set.")
    profile_path = os.path.join(zetta_root, ".zetta/profile")

    try:
        config = configparser.ConfigParser()
        config.read(profile_path)
        user = config.get('default', 'user_name', fallback=None)
    except FileNotFoundError:
        print(f"File not found: {profile_path}")
    except IOError:
        print(f"An error occurred while reading the file: {profile_path}")

    GITEA_HISTORY_URL = f"{SERVICE_GITEA_URL}/api/v1/repos/{user}/{dataset_name}/commits"
    params = {
        "stat": "false",
        "verification": "false",
        "files": "false"
    }
    response = requests.get(GITEA_HISTORY_URL, params=params)

    if response.status_code == 200:
        commit_histories = response.json()[:num_commits]
        for commit in commit_histories:
            print(f"{commit['sha'][:7]} {commit['commit']['message'].strip()}")
    else:
        response.raise_for_status()


@dataset_cli.command(name="register", help="register dataset.")
@synchronizer.create_blocking
async def register(json: bool = False):
    pass
