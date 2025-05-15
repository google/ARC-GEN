# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""A command-line interface for ARC-GEN."""

import json
import random
import sys
import task_list

ARC_AGI_DATA_DIR = "external/ARC-AGI/data/training/"


def validate_generators():
  """Validates all generators against their expected outputs."""
  passing, failing = 0, []
  for _, task_info in task_list.task_list().items():
    task_id, _, validator = task_info
    actual_result = validator()
    with open(ARC_AGI_DATA_DIR + task_id + ".json", "r") as f:
      expected_result = json.load(f)
      if "name" in expected_result: del expected_result["name"]
      if actual_result == expected_result:
        passing += 1
      else:
        failing.append(task_id)
  print("A total of " + str(passing) + " generators passed.")
  print("A total of " + str(len(failing)) + " generators failed.")
  if failing: print("Failing generators: " + str(failing))


def generate_benchmarks(task_num, num_examples):
  """Creates a benchmark suite for a given task."""
  task_info = task_list.task_list()[task_num]
  _, generator, _ = task_info
  examples = []
  for example_id in range(num_examples):
    random.seed(task_num + example_id)
    examples.append(generator())
  print(examples)


def main(argv) -> None:
  if argv[1] == "generate": generate_benchmarks(int(argv[2]), int(argv[3]))
  if argv[1] == "validate": validate_generators()


if __name__ == "__main__":
  main(sys.argv)
