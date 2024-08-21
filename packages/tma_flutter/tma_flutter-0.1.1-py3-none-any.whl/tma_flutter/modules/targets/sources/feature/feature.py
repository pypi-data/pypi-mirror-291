import typer, os
from typing_extensions import Annotated
from pathlib import Path
from tma_flutter.snippets.sources import flutter, template


app = typer.Typer()


@app.command(name="make")
def make_target(
    feature_name: Annotated[str, typer.Argument()],
    dir_name: Annotated[str, typer.Argument()] = "features",
):
    flutter.create_package(
        package_name=feature_name,
        dir_name=dir_name,
    )


def name(project_name: str) -> str:
    return project_name


def copy_template(
    feature_name: str,
    interface_name: str,
):
    feature_path = _get_feature_path()
    lib_path = feature_path.joinpath("lib")
    test_path = feature_path.joinpath("test")
    template.remove_dir_content(lib_path)
    template.remove_dir_content(test_path)

    template_path = Path(__file__).absolute().parent.joinpath("templates")
    template.copy(
        copy_file_parent_path=template_path.joinpath("lib"),
        file_name="feature.dart",
        to_save_path=lib_path.joinpath(f"{feature_name}.dart"),
        template_variables={
            "interface_snake": interface_name,
        },
    )


def add_dependency(interface_name: str):
    feature_path = _get_feature_path()
    os.chdir(feature_path)
    flutter.add_dependency(
        target_name=interface_name,
        target_path="../interfaces",
    )
    os.chdir(feature_path.parent)
    return


def _get_feature_path() -> Path:
    return Path(os.getcwd()).joinpath("features")


if __name__ == "__main__":
    app()
