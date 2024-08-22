import typer
from typing_extensions import Annotated
from tma_flutter.modules.layers.sources import helper


app = typer.Typer()
presentation = "presentation"


@app.command(name="make")
def make_module(project_name: Annotated[str, typer.Argument()]):
    helper.make_presentation_module(project_name)


if __name__ == "__main__":
    app()
