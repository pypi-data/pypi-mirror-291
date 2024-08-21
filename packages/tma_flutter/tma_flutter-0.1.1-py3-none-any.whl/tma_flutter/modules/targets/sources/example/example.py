import typer, os
from typing_extensions import Annotated
from pathlib import Path
from tma_flutter.snippets.sources import flutter, template


app = typer.Typer()


@app.command(name="make")
def make_target(
    example_name: Annotated[str, typer.Argument()],
    dir_name: Annotated[str, typer.Argument()] = "examples",
):
    flutter.create_app(
        app_name=example_name,
        dir_name=dir_name,
    )


def name(project_name: str) -> str:
    return project_name + "_" + "example"


def copy_template(
    example_name: str,
    view_name: str,
):
    example_path = get_example_path()
    lib_path = example_path.joinpath("lib")
    test_path = example_path.joinpath("test")
    template.remove_dir_content(lib_path)
    template.remove_dir_content(test_path)

    template_path = Path(__file__).absolute().parent.joinpath("templates")
    template.copy(
        copy_file_parent_path=template_path.joinpath("lib"),
        file_name="main.dart",
        template_variables={
            "example_snake": example_name,
            "example_pascal": template.pascal_case(example_name),
        },
        to_save_path=lib_path.joinpath(f"main.dart"),
    )
    template.copy(
        copy_file_parent_path=template_path.joinpath("lib"),
        file_name="example.dart",
        template_variables={
            "example_pascal": template.pascal_case(example_name),
            "view_snake": view_name,
            "view_pascal": template.pascal_case(view_name),
        },
        to_save_path=lib_path.joinpath(f"{example_name}.dart"),
    )


def add_view_dependency(view_name: str):
    example_path = get_example_path()
    os.chdir(example_path)
    flutter.add_dependency(
        target_name=view_name,
        target_path="../views",
    )
    os.chdir(example_path.parent)


def get_example_path() -> Path:
    return Path(os.getcwd()).joinpath("examples")


if __name__ == "__main__":
    app()
