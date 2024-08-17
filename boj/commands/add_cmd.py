import json
import os
import time
from rich import print
from rich.console import Console

from boj.core.solved import solvedAPI

console = Console()

def create_level_folder(problem_id: int, rank: list[str, str], lang="python") -> None:
    created = False

    level_part, level_num = rank
    directory_path = os.path.join(level_part, level_num, str(problem_id))
    os.makedirs(directory_path, exist_ok=True)
    with open("boj/settings/language.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        extension = data[lang]
    file_path = os.path.join(directory_path, f"main{extension}")
    with console.status("Checking file existence...") as status:
        time.sleep(0.1)
        if not os.path.exists(file_path):
            status.update("No file exists. Creating file...")
            open(file_path, "w", encoding="utf-8").close()
            created = True
            time.sleep(0.1)
        else:
            status.update(f"{file_path} already exists.")
            time.sleep(0.1)

    if created:
        print(f"{file_path} successfully created!")
    elif not created:
        print(f"successfully ended.")


def new_problem(id, lang="PyPy3"):
    try:
        solvedAPI.load_rank_info()
        response = solvedAPI.fetch_problem_info(id)

        problem_id, _, level = solvedAPI.parse_problem_info(response)
        create_level_folder(problem_id, level, lang)
    except Exception as e:
        print(f"[bold red]Error : {e}[/bold red]")
