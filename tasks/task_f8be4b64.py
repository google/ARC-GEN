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


def generate(size=None, rows=None, cols=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: The size of the grid.
    rows: The rows of the crosses.
    cols: The columns of the crosses.
    colors: The colors of the crosses.
  """

  def draw():
    # We'll use -1 as the background for now.
    grid, output = common.grids(size, size, -1)
    # First, draw the crosses on the input & output grids.
    for row, col, color in zip(rows, cols, colors):
      output[row][col] = grid[row][col] = color
      for dr, dc in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
        output[row + dr][col + dc] = grid[row + dr][col + dc] = 3
    # Second, extend the crosses as far as they can go.
    seen_green = False
    for row, col, color in zip(rows, cols, colors):
      for r in range(row + 2, size):
        if output[r][col] == 3:
          seen_green = True
          break
        output[r][col] = color
      for r in range(row - 2, -1, -1):
        if output[r][col] == 3:
          seen_green = True
          break
        output[r][col] = color
      for c in range(col + 2, size):
        if output[row][c] == 3:
          seen_green = True
          break
        if output[row][c] == -1: output[row][c] = color
      for c in range(col - 2, -1, -1):
        if output[row][c] == 3:
          seen_green = True
          break
        if output[row][c] == -1: output[row][c] = color
    # Third, convert the -1's to zeros.
    grid = [[max(0, color) for color in row] for row in grid]
    output = [[max(0, color) for color in row] for row in output]
    return grid, output, seen_green

  if size is None:
    size = common.randint(10, 30)
    num_crosses = common.randint(2, min(5, size // 3))
    colors = common.sample([0, 1, 2, 4, 5, 6, 7, 8, 9], num_crosses)
    seen_green = common.randint(0, 1)
    while True:
      rows = common.sample(list(range(2, size - 2)), num_crosses)
      cols = common.sample(list(range(2, size - 2)), num_crosses)
      if not common.overlaps(rows, cols, [3] * num_crosses, [3] * num_crosses):
        break
      _, _, sg = draw()
      if sg == seen_green: break

  grid, output, _ = draw()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=18, rows=[2, 7, 11, 15], cols=[3, 13, 7, 14], colors=[0, 5, 6, 4]),
      generate(size=10, rows=[2, 3, 6], cols=[2, 8, 5], colors=[5, 6, 8]),
      generate(size=13, rows=[3, 9], cols=[3, 8], colors=[2, 0]),
      generate(size=30, rows=[3, 4, 18, 21], cols=[5, 20, 13, 22], colors=[2, 6, 0, 8]),
  ]
  test = [
      generate(size=19, rows=[3, 4, 10, 12, 14], cols=[6, 13, 8, 14, 3], colors=[8, 4, 0, 1, 2]),
  ]
  return {"train": train, "test": test}
