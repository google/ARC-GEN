# Copyright 2026 Google LLC
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


def generate(colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    colors: A list of colors to use.
  """

  if colors is None:
    grid = common.grid(10, 10)
    for row in range(10):
      for col in range(10):
        if common.randint(0, 9) == 0:
          grid[row][col] = grid[row][9 - col] = 5
        elif common.randint(0, 9) == 0:
          grid[row][col] = 5
    colors = common.flatten(grid)

  grid, output = common.grids(10, 10)
  for i, color in enumerate(colors):
    grid[i // 10][i % 10] = color
  for row in range(10):
    for col in range(10):
      if not grid[row][col]: continue
      output[row][col] = 1 if grid[row][9 - col] else 5
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors=[0, 0, 0, 0, 0, 5, 0, 0, 0, 0,
                       0, 5, 0, 0, 0, 0, 0, 0, 5, 5,
                       0, 0, 0, 5, 5, 5, 5, 0, 0, 0,
                       0, 0, 0, 0, 5, 5, 0, 0, 0, 0,
                       0, 0, 0, 0, 5, 0, 0, 0, 0, 0,
                       0, 0, 5, 0, 0, 0, 0, 5, 0, 0,
                       0, 0, 0, 0, 0, 5, 0, 0, 0, 0,
                       0, 0, 5, 0, 5, 5, 5, 0, 0, 0,
                       0, 5, 0, 0, 5, 5, 0, 0, 5, 0,
                       5, 0, 0, 0, 5, 5, 0, 0, 0, 5]),
      generate(colors=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 5, 5, 0, 0, 0, 0,
                       0, 0, 0, 0, 5, 5, 0, 0, 0, 0,
                       0, 0, 0, 5, 5, 5, 5, 0, 0, 0,
                       0, 0, 0, 0, 5, 0, 0, 5, 0, 0,
                       5, 0, 0, 0, 0, 0, 0, 0, 0, 5,
                       0, 0, 0, 0, 5, 5, 5, 0, 0, 0,
                       0, 5, 0, 5, 5, 5, 5, 0, 0, 0,
                       0, 0, 0, 5, 5, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
      generate(colors=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 5, 0, 0, 5, 5, 0, 0, 5, 0,
                       0, 0, 0, 5, 0, 0, 5, 0, 0, 0,
                       0, 0, 5, 0, 0, 0, 0, 5, 0, 0,
                       0, 0, 0, 5, 0, 5, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 5, 0, 0, 0, 0,
                       0, 0, 0, 0, 5, 5, 0, 0, 0, 0,
                       5, 0, 0, 0, 5, 5, 0, 0, 0, 5,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 5, 0, 0, 0, 0, 0, 5]),
      generate(colors=[0, 0, 5, 0, 0, 0, 5, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 5, 0, 0, 0,
                       0, 0, 0, 0, 5, 0, 0, 0, 0, 0,
                       0, 0, 5, 5, 5, 5, 5, 5, 0, 0,
                       0, 0, 0, 5, 0, 0, 0, 5, 0, 0,
                       0, 0, 0, 0, 5, 5, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
  ]
  test = [
      generate(colors=[0, 5, 0, 0, 0, 0, 0, 0, 5, 0,
                       0, 0, 0, 0, 5, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 5, 0, 0, 0, 0, 0,
                       0, 5, 0, 0, 0, 0, 0, 5, 0, 0,
                       0, 0, 0, 0, 5, 5, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 5, 0, 0, 0, 0,
                       0, 5, 0, 5, 5, 5, 5, 0, 5, 0,
                       0, 0, 0, 0, 5, 5, 0, 0, 0, 0,
                       0, 0, 0, 5, 5, 5, 5, 5, 0, 0,
                       0, 0, 5, 5, 5, 5, 5, 0, 0, 0]),
  ]
  return {"train": train, "test": test}
