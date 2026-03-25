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

"""Generator."""


import common


def generate(lengths=None):
  """Returns input and output grids according to the given parameters.

  Args:
    lengths: the lengths of the columns
  """
  if lengths is None:
    lengths = [common.randint(2, 10) for _ in range(4)]

  width, height = 2 * len(lengths) + 1, max(lengths) + 1
  grid, output = common.grids(width, height)
  for idx, length in enumerate(lengths):
    for i in range(length):
      r, c = height - i - 1, 2 * idx + 1
      output[r][c] = grid[r][c] = common.red()
    for i in range(length // 2):
      r, c = height - i - 1, 2 * idx + 1
      output[r][c] = common.cyan()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(lengths=[6, 5, 4, 3]),
      generate(lengths=[7, 5, 3, 6]),
      generate(lengths=[7, 3, 4, 8]),
  ]
  test = [
      generate(lengths=[10, 9, 2, 5]),
  ]
  return {"train": train, "test": test}
