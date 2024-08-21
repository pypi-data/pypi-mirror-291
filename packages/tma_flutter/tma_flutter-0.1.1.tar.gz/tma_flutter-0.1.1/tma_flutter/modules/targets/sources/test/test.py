import typer, os
from typing_extensions import Annotated
from pathlib import Path
from tma_flutter.snippets.sources import flutter, template


app = typer.Typer()


@app.command(name="make")
def make_target(
    test_name: Annotated[str, typer.Argument()],
    dir_name: Annotated[str, typer.Argument()] = "tests",
):
    flutter.create_package(
        package_name=test_name,
        dir_name=dir_name,
    )


def name(project_name: str) -> str:
    return project_name + "_" + "test"


def copy_template(feature_name: str):
    test_path = _get_test_path()
    lib_path = test_path.joinpath("lib")
    test_path = test_path.joinpath("test")
    template.remove_dir_content(lib_path)
    template.remove_dir_content(test_path)

    template_path = Path(__file__).absolute().parent.joinpath("templates")
    template.copy(
        copy_file_parent_path=template_path.joinpath("lib"),
        file_name="feature_testing.dart",
        to_save_path=lib_path.joinpath(f"{feature_name}_testing.dart"),
    )
    template.copy(
        copy_file_parent_path=template_path.joinpath("test"),
        file_name="feature_test.dart",
        to_save_path=test_path.joinpath(f"{feature_name}_test.dart"),
        template_variables={
            "feature_snake": feature_name,
        },
    )


def add_dependency(
    feature_name: str,
    interface_name: str,
):
    test_path = _get_test_path()
    os.chdir(test_path)
    flutter.add_dependency(
        target_name=feature_name,
        target_path="../features",
    )
    flutter.add_dependency(
        target_name=interface_name,
        target_path="../interfaces",
    )
    os.chdir(test_path.parent)


def _get_test_path() -> Path:
    return Path(os.getcwd()).joinpath("tests")


if __name__ == "__main__":
    app()
