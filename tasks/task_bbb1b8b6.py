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
    size: The size of the grid.
    rows: The rows of the boxes.
    cols: The columns of the boxes.
    thicks: The thicknesses of the boxes.
  """

  if colors is None:
    color = common.random_color(exclude=[1, 5])
    grid = common.grid(9, 4)
    while True:
      pattern = [common.randint(0, 1) for _ in range(16)]
      if sum(pattern) >= 4 and sum(pattern) <= 12: break
    other = [1 - p for p in pattern]
    if common.randint(0, 1):
      while True:
        other = [common.randint(0, 1) for _ in range(16)]
        if sum(other) >= 4 and sum(other) <= 12: break
    for r in range(4): grid[r][4] = 5
    for i, p in enumerate(pattern):
      grid[i // 4][i % 4] = p
    for i, p in enumerate(other):
      grid[i // 4][i % 4 + 5] = p * color
    colors = common.flatten(grid)

  grid, output = common.grid(9, 4), common.grid(4, 4)
  for i, color in enumerate(colors):
    grid[i // 9][i % 9] = color
  exact = True
  for r in range(4):
    for c in range(4):
      if (grid[r][c] == 0) == (grid[r][c + 5] == 0): exact = False
  for r in range(4):
    for c in range(4):
      output[r][c] = grid[r][c] + (grid[r][c + 5] if exact else 0)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors=[1, 1, 1, 1, 5, 0, 0, 0, 0,
                       1, 0, 0, 1, 5, 0, 6, 6, 0,
                       1, 0, 0, 1, 5, 0, 6, 6, 0,
                       1, 1, 1, 1, 5, 0, 0, 0, 0]),
      generate(colors=[1, 1, 1, 1, 5, 2, 2, 0, 0,
                       1, 0, 0, 1, 5, 2, 2, 0, 0,
                       1, 0, 0, 1, 5, 0, 0, 0, 0,
                       1, 1, 1, 1, 5, 0, 0, 0, 0]),
      generate(colors=[1, 1, 1, 1, 5, 0, 0, 0, 0,
                       1, 0, 0, 0, 5, 0, 7, 7, 7,
                       1, 0, 1, 1, 5, 0, 7, 0, 0,
                       1, 0, 1, 0, 5, 0, 7, 0, 7]),
      generate(colors=[0, 0, 0, 1, 5, 2, 2, 0, 0,
                       1, 0, 0, 0, 5, 2, 2, 0, 0,
                       1, 1, 0, 0, 5, 0, 2, 2, 0,
                       1, 1, 1, 0, 5, 0, 2, 2, 0]),
      generate(colors=[1, 1, 0, 0, 5, 0, 0, 3, 3,
                       1, 0, 0, 1, 5, 0, 3, 3, 0,
                       1, 0, 0, 1, 5, 0, 3, 3, 0,
                       1, 1, 0, 0, 5, 0, 0, 3, 3]),
      generate(colors=[1, 1, 1, 1, 5, 3, 3, 0, 0,
                       1, 0, 0, 1, 5, 3, 3, 0, 0,
                       1, 0, 0, 1, 5, 3, 0, 0, 0,
                       1, 0, 0, 1, 5, 0, 0, 0, 0]),
      generate(colors=[0, 0, 0, 1, 5, 2, 2, 2, 0,
                       1, 0, 0, 0, 5, 0, 2, 2, 2,
                       1, 1, 0, 0, 5, 0, 0, 2, 2,
                       1, 1, 1, 0, 5, 0, 0, 0, 2]),
  ]
  test = [
      generate(colors=[1, 1, 1, 1, 5, 2, 0, 0, 0,
                       0, 1, 1, 0, 5, 2, 2, 2, 2,
                       0, 1, 1, 0, 5, 2, 0, 0, 0,
                       0, 0, 0, 0, 5, 0, 0, 0, 0]),
      generate(colors=[1, 1, 0, 0, 5, 0, 0, 3, 3,
                       1, 0, 0, 1, 5, 0, 3, 3, 0,
                       0, 0, 0, 1, 5, 3, 3, 3, 0,
                       0, 1, 1, 1, 5, 3, 0, 0, 0]),
  ]
  return {"train": train, "test": test}
