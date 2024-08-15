import os
import time
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from bs4 import BeautifulSoup
import requests

from utils.solved import solvedAPI
from utils.log import console

class ProblemFetcher:
    def __init__(self, problem_id):
        self.problem_id = problem_id
        self.input_list = []
        self.output_list = []

    def fetch(self):
        problem_info = solvedAPI.fetch_problem_info(self.problem_id)
        level_title, level_num = solvedAPI.parse_problem_info(problem_info)[2]

        base_path = f"{level_title}/{level_num}/{self.problem_id}"
        page_content = self._fetch_problem_page()  # Fetch the problem page content
        soup = BeautifulSoup(page_content, "html.parser")
        self.input_list, self.output_list = self._parse_sample_data(soup, base_path)

    def _fetch_problem_page(self):
        url = f"https://www.acmicpc.net/problem/{self.problem_id}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            raise Exception(f"Error fetching problem page: {response.status_code}")

        return response.text

    def _parse_sample_data(self, soup, base_path):
        sample_data = soup.find_all(class_="sampledata")
        input_list = []
        output_list = []

        # Check if sample_data is empty or not
        if not sample_data:
            raise Exception("Sample data not found. The HTML structure might have changed.")

        os.makedirs(f"./{base_path}/data", exist_ok=True)
        for elem in sample_data:
            index = elem.get("id")[-1]
            content = elem.get_text(strip=True)

            if "input" in elem.get("id"):
                input_list.append(index)
                self._write_to_file(f"./{base_path}/data/{index}.in", content)
            elif "output" in elem.get("id"):
                output_list.append(index)
                self._write_to_file(f"./{base_path}/data/{index}.out", content)

        return input_list, output_list

    def _write_to_file(self, filepath, content):
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)


class TestRunner:
    def __init__(self, problem_id, input_list, output_list):
        problem_info = solvedAPI.fetch_problem_info(problem_id)
        level_title, level_num = solvedAPI.parse_problem_info(problem_info)[2]

        self.problem_id = problem_id
        self.base_path = f"{level_title}/{level_num}/{self.problem_id}"
        self.input_list = input_list
        self.output_list = output_list
        self.results = []

    def run_tests(self):
        with ThreadPoolExecutor() as executor:
            future_to_index = {
                executor.submit(self._execute_test_case, index): index
                for index in self.input_list
            }
            for future in as_completed(future_to_index):
                index = future_to_index[future]
                self._update_console_status(future, index)

        self._evaluate_results()

    def _update_console_status(self, future, index):
        with console.status("Loading inputs...") as status:
            status.update(f"Test Case #{index} : [bold green]RUNNING[/]")
            try:
                result = future.result()
                self.results.append((index, result))
            except Exception as e:
                console.print(f"[bold red]Error in test Case #{index}: {e}[/bold red]")
            time.sleep(1)

    def _evaluate_results(self):
        corrects = []

        for index, (actual_output, expected_output, input_value) in self.results:
            actual_output_lines = actual_output.strip().splitlines()
            expected_output_lines = expected_output.strip().splitlines()

            if actual_output_lines == expected_output_lines:
                self._print_result(index, actual_output, expected_output, input_value, "green")
                corrects.append(True)
            else:
                self._print_result(index, actual_output, expected_output, input_value, "red")
                corrects.append(False)

        self._print_summary(corrects)

    def _print_result(self, index, actual_output, expected_output, input_value, color):
        console.print(f"[bold {color}]---------------------------------------------------[/bold {color}]")
        console.print(f"[bold deep_sky_blue1]Test Case #{index} :[/bold deep_sky_blue1] [bold {color}]OUTPUT[/bold {color}]")
        console.print(f"[bold magenta]Input:[/bold magenta] \n{input_value.strip()}\n")
        console.print(f"[bold magenta]Expected:[/bold magenta] \n{expected_output.strip()}")
        console.print(f"[bold magenta]Yours:[/bold magenta] \n{actual_output.strip()}")

    def _print_summary(self, corrects):
        final_color = "green" if all(corrects) else "red"
        console.print(f"[bold {final_color}]---------------------------------------------------[/]")
        console.print("\n[bold green]All tests completed![/bold green]")

        for count, correct in enumerate(corrects, start=1):
            status = "PASS" if correct else "FAILED"
            color = "green" if correct else "red"
            console.print(f"[bold deep_sky_blue1]- Test Case #{count} :[/] [bold {color}]{status}[/]")

    def _execute_test_case(self, index):
        input_file = f"./{self.base_path}/data/{index}.in"
        expected_output_file = f"./{self.base_path}/data/{index}.out"

        actual_output = self._execute_solution(input_file)
        expected_output = self._read_file(expected_output_file)
        input_value = self._read_file(input_file)

        return actual_output, expected_output, input_value

    def _execute_solution(self, input_file):
        # Determine the file type and set the command accordingly
        solution_files = [f for f in os.listdir(f"./{self.base_path}") if os.path.isfile(os.path.join(f"./{self.base_path}", f))]
        solution_file = None

        for file in solution_files:
            if any(file.endswith(ext) for ext in [".py", ".cpp", ".c", ".go", ".cs", ".js", ".ts"]):
                solution_file = file
                break

        if not solution_file:
            raise Exception("No solution file found!")

        file_ext = os.path.splitext(solution_file)[1]

        command = []
        if file_ext == ".py":
            command = ["python3", f"./{self.base_path}/{solution_file}"]
        elif file_ext == ".cpp":
            executable = f"./{self.base_path}/{solution_file.replace('.cpp', '')}"
            subprocess.run(["g++", f"./{self.base_path}/{solution_file}", "-o", executable, "-std=c++17"])
            command = [executable]
        elif file_ext == ".c":
            executable = f"./{self.base_path}/{solution_file.replace('.c', '')}"
            subprocess.run(["gcc", f"./{self.base_path}/{solution_file}", "-o", executable, "-std=c99"])
            command = [executable]
        elif file_ext == ".go":
            command = ["go", "run", f"./{self.base_path}/{solution_file}"]
        elif file_ext == ".cs":
            executable = f"./{self.base_path}/{solution_file.replace('.cs', '.exe')}"
            subprocess.run(["csc", "-out:" + executable, f"./{self.base_path}/{solution_file}"])
            command = [executable]
        elif file_ext == ".js":
            command = ["node", f"./{self.base_path}/{solution_file}"]
        elif file_ext == ".ts":
            js_output_file = f"./{self.base_path}/{solution_file.replace('.ts', '.js')}"
            subprocess.run(["tsc", f"./{self.base_path}/{solution_file}"])
            command = ["node", js_output_file]

        process = subprocess.Popen(
            command,
            stdin=open(input_file, "r"),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        stdout, _ = process.communicate()
        return stdout.decode("utf-8").strip()

    def _read_file(self, filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read().strip()


class TestCaseExecutor:
    def __init__(self, problem_id):
        self.problem_id = problem_id

    def execute(self):
        fetcher = ProblemFetcher(self.problem_id)
        fetcher.fetch()
        runner = TestRunner(self.problem_id, fetcher.input_list, fetcher.output_list)
        runner.run_tests()


if __name__ == "__main__":
    solvedAPI.load_rank_info()
    executor = TestCaseExecutor(1000)
    executor.execute()
