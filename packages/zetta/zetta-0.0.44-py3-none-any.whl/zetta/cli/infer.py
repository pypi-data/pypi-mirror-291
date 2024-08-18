# Copyright ZettaBlock Labs 2024
import typer
import requests
import json
from zetta._utils.async_utils import synchronizer

from openai import OpenAI

API_SERVER = "http://ec2-44-197-238-205.compute-1.amazonaws.com:8000"

infer_cli = typer.Typer(
    name="infer",
    help="Send inference requests to Zetta AI network.",
    no_args_is_help=True,
)


@infer_cli.command(
    name="list",
    help="List all the visible inference endpoints for a network.",
)
@synchronizer.create_blocking
async def list(model: str = "all"):
    url = f"{API_SERVER}/infer/list"
    response = requests.get(url, params={"model": model})
    if response.status_code == 200:
        data = response.json()
        print(json.dumps(data, indent=2))
    else:
        response.raise_for_status()


@infer_cli.command(
    name="status", help="Show the stats information of the inference endpoints."
)
@synchronizer.create_blocking
async def status(endpoint: str = "all"):
    url = f"{API_SERVER}/infer/status"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        print(json.dumps(data, indent=2))
    else:
        response.raise_for_status()


@infer_cli.command(name="shell", help="Open a shell to chat with model")
@synchronizer.create_blocking
async def shell(model: str = "", endpoint: str = "any"):
    pass


@infer_cli.command(name="chat", help=" chat with model")
@synchronizer.create_blocking
async def chat(model: str = "", msg: str = "", endpoint: str = "any"):
    client = OpenAI(
        base_url="http://ec2-44-197-238-205.compute-1.amazonaws.com:8888/v1",
        api_key="token-abc123",
    )
    completion = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": msg,
            },
        ],
    )
    print(completion.choices[0].message.content)
    pass


@infer_cli.command(
    name="history",
    help="Check the inference history. ",
)
@synchronizer.create_blocking
async def history(
    model: str = "", endpoint: str = "any", inputs: str = "", delimiter: str = ""
):
    pass
