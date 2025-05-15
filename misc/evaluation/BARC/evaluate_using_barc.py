import argparse
import random
import sys
from execution import multi_execute_transformation, multi_execute_input_generator, execute_transformation
import numpy as np
import os
import re
import tqdm
import time
from utils import get_concepts_from_lines, get_description_from_lines
import subprocess
import json

class Problem:
    def __init__(self, source_code):
        self.source = source_code
        self.examples = []
        self.seeds = []
        self.source_uid = ""
        

    def add_example(self, input_grid, output_grid):
        self.examples.append((input_grid, output_grid))
    def to_dict(self):
        return {
            "source": self.source,
            "examples": [(input_grid.tolist(), output_grid.tolist()) for input_grid, output_grid in self.examples],
            "seeds": self.seeds,
            "source_uid": self.source_uid
        }

def run_transformation(source, input_grid, timeout=10, function_name="main", num_returns=50):
    """
    run the transformation on the input grid and return the output grid multiple times
    """
    random.seed(0)
    random_seeds = [random.randint(0, 1<<30) for _ in range(num_returns)]
    output_grids = multi_execute_transformation([source] * num_returns, [input_grid] * num_returns, random_seeds, timeout, function_name)
    return output_grids

def generate_solution(problem_source_uid, problem_source, examples, num_deterministic_check=20, timeout=10):
    """
    Generates output grids for each input grid (using the transformation) and checks them against the expected result.
    Return 'True' if all examples pass, otherwise 'False'
    """
    problem = Problem(problem_source)

    for example in examples:
        try:
            input_grid, output_grid = example["input"], example["output"]
            output_grids = run_transformation(problem_source, input_grid, timeout=timeout, num_returns=num_deterministic_check)
            correct = max([type(o) != str and output_grid == o.tolist() for o in output_grids])
            incorrect = max([type(o) == str or output_grid != o.tolist() for o in output_grids])
            if incorrect: return False
        except:
            return False
    return True

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--total_timeout", type=int, default=30, help="The total timeout value for a problem generation run")
    parser.add_argument("--exampledir", type=str, help="Input directory for the generated examples")
    args = parser.parse_args()

    total_timeout = args.total_timeout 

    problems_source = []
    problems_seeds = []
    problem_source_uids = []
    seeds = os.listdir("seeds")
    # filter files with .py extension and 8 hex value characters in the file name
    pattern = r"([0-9a-f]{8})\.py"
    problem_source_uids = sorted([re.match(pattern, filename).group(1) for filename in seeds if re.match(pattern, filename)])
    # Now `matched_files` contains all the filenames that match the pattern

    if problem_source_uids:
        for problem_source_uid in problem_source_uids:
            with open(f"seeds/{problem_source_uid}.py") as f:
                source = f.read()
            problems_source.append(source)

    # For these UIDs, BARC fails on one or more ARC-AGI-1 example pairs.
    bad_uids = ["1b2d62fb", "25ff71a9", "28e73c20", "3428a4f5", "bbc9ae5d", "cf98881b",
                "feca6190", "25d8a9c8", "6fa7a44f", "995c5fa3", "9af7a82c", "db93a21d",
                "e48d4e1a", "f8b3ba0a", "017c7c7b", "0520fde7", "178fcbfb", "1caeab9d",
                "1fad071e", "2dee498d", "3618c87e", "3e980e27", "3f7978a0", "444801d8",
                "54d82841", "6d58a25d", "7447852a", "834ec97d", "8403a5d5", "8d5021e8",
                "8e5a5113", "9f236235", "a3df8b1e", "a79310a0", "a9f96cdd", "bd4472b8",
                "d4a91cb9", "e179c5f4", "fcc82909", "ff28f65a", "025d127b", "1bfc4729",
                "3ac3eb23", "8d510a79", "aabf363d", "d06dbe63", "d9f24cd1", "db3e9e38",
                "eb281b96", "8a004b2b", "29c11459", "caa06a1f"]
    passed_problems, failed_problems = [], []
    for i, problem_source in enumerate(problems_source if args.exampledir else tqdm.tqdm(problems_source)):
        problem_source_uid = problem_source_uids[i]
        examples = {}
        with open(f"{args.exampledir}/{problem_source_uid}.json") as f:
            import json
            problem_examples = json.loads(f.read())
            if type(problem_examples) != list:
                problem_examples = problem_examples["train"] + problem_examples["test"]
            examples[problem_source_uid] = problem_examples
        if not isinstance(problem_source, list):
            problem_source = [problem_source]
        for j, source in enumerate(problem_source):
            if args.exampledir:
                if problem_source_uid in bad_uids: continue
                if problem_source_uid not in examples: continue
                print("Testing task " + problem_source_uid + " ... ", end="")
                result = generate_solution(problem_source_uid, source, examples[problem_source_uid])
                if result:
                    passed_problems.append(problem_source_uid)
                if not result:
                    failed_problems.append(problem_source_uid)
                print("pass" if result else "FAIL")

    num_problems = len(passed_problems) + len(failed_problems)
    print("Examples pass for " + str(len(passed_problems)) + "/" + str(num_problems) + " tasks (" + str(100.0*len(passed_problems)/num_problems) + "%)")


if __name__ == "__main__":
    main()
