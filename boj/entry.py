import argparse

from .add_cmd import new_problem
from .test_cmd import TestCaseExecutor
from .utils.solved import solvedAPI


def cli():
    parser = argparse.ArgumentParser(description="CLI for managing problems.")
    subparsers = parser.add_subparsers(dest="command")

    # 'add' 명령어
    add_parser = subparsers.add_parser("add", help="Add a new problem")
    add_parser.add_argument("problem_id", type=int, help="The ID of the problem")
    add_parser.add_argument(
        "-l",
        "--lang",
        type=str,
        help="Programming language (e.g., C++17)",
        default="PyPy3",
    )

    test_parser = subparsers.add_parser("test", help="test a problem")
    test_parser.add_argument("problem_id", type=int, help="The ID of the problem")
    test_parser.add_argument(
        "-l",
        "--lang",
        type=str,
        help="Programming language (e.g., C++17)",
        default="PyPy3",
    )

    args = parser.parse_args()

    if args.command == "add":
        new_problem(args.problem_id, args.lang)
    if args.command == "test":
        solvedAPI.load_rank_info()
        executor = TestCaseExecutor(1000)
        executor.execute()


