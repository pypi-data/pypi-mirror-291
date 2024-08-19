# Copyright ZettaBlock Labs 2024
import typer
from zetta._utils.async_utils import synchronizer

huggingface_cli = typer.Typer(
    name="hf",
    help="Integration with huggingface.",
    no_args_is_help=True,
)


@huggingface_cli.command(name="import-token", help="import a new huggingface token")
@synchronizer.create_blocking
async def import_token(json: bool = False):
    pass


@huggingface_cli.command(name="auth", help="Authorize the huggingface access.")
@synchronizer.create_blocking
async def auth(json: bool = False):
    pass


@huggingface_cli.command(
    name="import", help="Import the huggingface model or data repo."
)
@synchronizer.create_blocking
async def import_repo(json: bool = False):
    pass
