import time
from typing import Dict, Tuple
import requests
import json
from rich.console import Console

console = Console()


class solvedAPI:
    rank_info: Dict[int, Tuple[str, str]] = {}

    @staticmethod
    def load_rank_info():
        with console.status("Load level.json...") as status:
            time.sleep(0.1)
        with open("boj/settings/level.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            solvedAPI.rank_info = {int(k): (v[0], v[1]) for k, v in data.items()}

    @staticmethod
    def fetch_problem_info(id: int):
        url = "https://solved.ac/api/v3/problem/show"

        querystring = {"problemId": f"{id}"}

        headers = {"x-solvedac-language": "ko", "Accept": "application/json"}
        with console.status("Get problem info...") as status:
            time.sleep(0.1)
            status.update(f"Get problem info from {url} with {querystring}, {headers}")
        response = requests.get(url, headers=headers, params=querystring)

        return response.json()

    @staticmethod
    def get_level(level):
        with console.status("Get level info...") as status:
            time.sleep(0.1)
        return solvedAPI.rank_info[level]

    @staticmethod
    def parse_problem_info(response):
        with console.status("Parsing problem info...") as status:
            time.sleep(0.1)
        return (
            response["problemId"],
            response["titleKo"],
            solvedAPI.get_level(response["level"]),
        )
