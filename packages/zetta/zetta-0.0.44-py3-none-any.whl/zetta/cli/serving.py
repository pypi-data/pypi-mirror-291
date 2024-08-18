# Copyright ZettaBlock Labs 2024
import requests
import typer
import json
from zetta._utils.async_utils import synchronizer


NEO_HOST = "https://neo-dev.prod.zettablock.com"
API_SERVER = "http://ec2-44-197-238-205.compute-1.amazonaws.com:8000"

serving_cli = typer.Typer(
    name="serving",
    help="Manage your inference serving in Zetta AI Network.",
    no_args_is_help=True,
)


@serving_cli.command(
    name="list",
    help="List all the visible inference endpoints that are currently running.",
)
@synchronizer.create_blocking
async def list(model: str = "all"):
    url = f"{API_SERVER}/serving/list"
    response = requests.get(url, params={"model": model})
    if response.status_code == 200:
        data = response.json()
        print(json.dumps(data, indent=2))
    else:
        response.raise_for_status()


@serving_cli.command(
    name="status", help="Show the stats information of the inference endpoints."
)
@synchronizer.create_blocking
async def status():
    url = f"{API_SERVER}/serving/status"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        print(json.dumps(data, indent=2))
    else:
        response.raise_for_status()


@serving_cli.command(name="deploy", help="Deploy a model for serving.")
@synchronizer.create_blocking
async def deploy(
    model: str = "", machine_type: str = "", duration: str = "", replica: int = 1
):
    url = f"{NEO_HOST}/v1/api/job"
    print(url)
    data = {"model_id": model, "type": "Model_Deployment", "version": "latest"}
    headers = {
        "X-API-KEY": "0538a29b-79f5-4700-9556-44609c5c2f1c",
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        print(response.json())
        return response.json()
    else:
        raise Exception(
            f"Failed to deploy model: [{response.status_code}] {response.text}"
        )


@serving_cli.command(name="renew", help="Renew a model for serving.")
@synchronizer.create_blocking
async def renew(model: str = "", duration: str = ""):
    pass


@serving_cli.command(name="update", help="Update a serving config")
@synchronizer.create_blocking
async def update(config: str):
    # machine type, replica and remain-time can be change here
    pass


@serving_cli.command(name="shell", help="Open a shell to chat with model")
@synchronizer.create_blocking
async def shell(model: str = "", endpoint: str = "any"):
    pass


@serving_cli.command(
    name="batch",
    help="Execuate batch inference for model, default delimiter is newline ",
)
@synchronizer.create_blocking
async def batch(
    model: str = "", endpoint: str = "any", inputs: str = "", delimiter: str = ""
):
    pass
