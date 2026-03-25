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

  def draw():
    grid, output = common.grids(10, 10, 7)
    for i, color in enumerate(colors):
      grid[i // 10][i % 10] = color
    for row in range(10):
      for col in range(10):
        if grid[row][col] != 6: continue
        num_left, num_right = 0, 0
        for c in range(0, col):
          if grid[row][c] != 7: num_left += 1
        for c in range(col + 1, 10):
          if grid[row][c] != 7: num_right += 1
        for c in range(col - num_left, col + num_right + 1):
          output[row][c] = 8
    return grid, output

  if colors is None:
    subset = common.sample([0, 1, 2, 3, 4, 5, 8, 9], common.randint(3, 8))
    grid = common.grid(10, 10, 7)
    freq = common.randint(1, 2)
    for row in range(10):
      for col in range(10):
        if common.randint(0, freq): continue
        grid[row][col] = common.choice(subset)
    for row in range(10):
      if common.randint(0, 1): continue
      grid[row][common.randint(0, 9)] = 6
    colors = common.flatten(grid)

  grid, output = draw()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors=[7, 7, 4, 7, 6, 7, 0, 7, 7, 7,
                       7, 5, 1, 3, 7, 7, 7, 7, 9, 1,
                       7, 2, 3, 7, 2, 7, 7, 7, 7, 7,
                       7, 8, 9, 7, 8, 7, 0, 7, 2, 8,
                       5, 9, 7, 1, 7, 5, 6, 8, 7, 8,
                       7, 2, 7, 0, 7, 7, 7, 1, 7, 6,
                       7, 7, 7, 7, 7, 7, 7, 7, 7, 4,
                       7, 7, 8, 7, 7, 4, 0, 7, 7, 5,
                       6, 7, 7, 7, 1, 2, 7, 7, 0, 4,
                       7, 7, 7, 7, 7, 2, 1, 7, 6, 7]),
      generate(colors=[7, 7, 7, 7, 7, 7, 7, 5, 7, 7,
                       7, 7, 9, 6, 7, 7, 2, 7, 7, 7,
                       7, 7, 7, 7, 7, 7, 7, 2, 9, 7,
                       2, 7, 9, 9, 7, 6, 7, 5, 7, 7,
                       7, 7, 7, 7, 7, 7, 7, 7, 7, 7,
                       7, 7, 7, 7, 7, 2, 7, 7, 7, 7,
                       7, 5, 9, 6, 7, 7, 7, 7, 7, 9,
                       7, 7, 7, 7, 7, 7, 7, 7, 7, 7,
                       7, 2, 7, 7, 7, 9, 7, 7, 7, 7,
                       7, 2, 2, 7, 7, 7, 7, 6, 7, 5]),
  ]
  test = [
      generate(colors=[0, 5, 7, 4, 7, 5, 1, 3, 7, 7,
                       7, 7, 7, 4, 4, 6, 5, 2, 7, 7,
                       4, 6, 2, 8, 7, 7, 8, 7, 0, 3,
                       1, 7, 7, 5, 3, 7, 6, 3, 7, 7,
                       0, 9, 7, 7, 7, 3, 7, 7, 7, 7,
                       7, 9, 3, 0, 7, 0, 5, 5, 3, 7,
                       7, 1, 7, 1, 7, 5, 5, 8, 7, 6,
                       7, 7, 7, 3, 3, 2, 7, 0, 9, 2,
                       7, 7, 0, 7, 6, 0, 7, 7, 1, 7,
                       1, 7, 4, 7, 1, 2, 7, 7, 1, 7]),
  ]
  return {"train": train, "test": test}
