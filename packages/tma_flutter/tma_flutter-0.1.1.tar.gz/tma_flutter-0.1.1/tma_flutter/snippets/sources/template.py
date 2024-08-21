import shutil
from pathlib import Path
from jinja2 import Environment, FileSystemLoader


def copy(
    copy_file_parent_path: Path,
    file_name: str,
    to_save_path: Path,
    template_variables: dict = {},
):
    env = Environment(loader=FileSystemLoader(copy_file_parent_path))
    template = env.get_template(file_name)
    template_str = template.render(template_variables)
    with open(to_save_path, "w") as f:
        f.write(template_str)


def remove_dir_content(dir_path: Path):
    shutil.rmtree(dir_path)
    dir_path.mkdir(parents=True, exist_ok=True)


def pascal_case(name: str) -> str:
    return "".join(x for x in name.title() if x != "_")
