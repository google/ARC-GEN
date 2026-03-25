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


def generate(size=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: The size of the grid.
    colors: The colors of the grid.
  """

  if size is None:
    size = common.randint(6, 9)
    while True:
      grid = common.grid(size, size, 7)
      # First, crawl along the left edge.
      for row in range(size - 2, 0, -1):
        if common.randint(0, 1) or common.get_pixel(grid, row + 1, 0) == 2:
          continue
        r, c = row, 0
        while True:
          if r >= size or c >= size: break
          grid[r][c] = 2
          if common.randint(0, 1) and common.get_pixel(grid, r + 2, c) != 2 and common.get_pixel(grid, r + 2, c - 1) != 2:
            r += 1
          else:
            c += 1
      # Second, crawl along the top edge.
      for col in range(0, size - 1):
        if common.randint(0, 1) or common.get_pixel(grid, 0, col - 1) == 2 or common.get_pixel(grid, 1, col - 1) == 2 or common.get_pixel(grid, 1, col) == 2:
          continue
        r, c = 0, col
        while True:
          if r >= size or c >= size: break
          grid[r][c] = 2
          if common.randint(0, 1) and common.get_pixel(grid, r + 2, c) != 2 and common.get_pixel(grid, r + 2, c - 1) != 2:
            r += 1
          else:
            c += 1
      if grid[size - 1][0] == 2 or grid[0][size - 1] == 2:
        continue  # Bottom left and top right corners must be open.
      colors = common.flatten(grid)
      if len(set(colors)) > 1: break  # Make sure we drew something.
    # Now, color the gaps grey and green.
    color = 0
    for row in range(size - 1, 0, -1):
      if grid[row][0] != 7: continue
      common.fill(grid, row, 0, 3 if color else 5)
      color = (color + 1) % 2
    for col in range(0, size):
      if grid[0][col] != 7: continue
      common.fill(grid, 0, col, 3 if color else 5)
      color = (color + 1) % 2
    colors = common.flatten(grid)

  grid, output = common.grids(size, size)
  for i, color in enumerate(colors):
    grid[i // size][i % size] = 2 if color == 2 else 7
    output[i // size][i % size] = color
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=7, colors=[3, 3, 2, 5, 5, 5, 5,
                               3, 3, 2, 2, 2, 5, 5,
                               3, 3, 3, 3, 2, 5, 5,
                               2, 2, 3, 3, 2, 2, 2,
                               5, 2, 3, 3, 3, 3, 3,
                               5, 2, 2, 2, 2, 3, 3,
                               5, 5, 5, 5, 2, 3, 3]),
      generate(size=7, colors=[2, 3, 3, 3, 3, 3, 3,
                               2, 3, 3, 3, 3, 3, 3,
                               2, 3, 3, 3, 3, 3, 3,
                               2, 2, 2, 3, 3, 3, 3,
                               5, 5, 2, 3, 3, 3, 3,
                               5, 5, 2, 2, 2, 3, 3,
                               5, 5, 5, 5, 2, 2, 2]),
      generate(size=8, colors=[5, 5, 5, 5, 5, 2, 3, 3,
                               5, 5, 5, 5, 5, 2, 3, 3,
                               2, 2, 2, 2, 5, 2, 3, 3,
                               3, 3, 3, 2, 5, 2, 3, 3,
                               3, 3, 3, 2, 5, 2, 3, 3,
                               2, 2, 3, 2, 5, 2, 2, 3,
                               5, 2, 3, 2, 5, 5, 2, 2,
                               5, 2, 3, 2, 5, 5, 5, 5]),
  ]
  test = [
      generate(size=9, colors=[3, 3, 3, 3, 3, 3, 3, 3, 3,
                               3, 3, 3, 3, 3, 3, 3, 3, 3,
                               2, 2, 2, 2, 2, 2, 2, 2, 3,
                               5, 5, 5, 5, 5, 5, 5, 2, 3,
                               2, 2, 2, 2, 2, 2, 5, 2, 2,
                               3, 3, 3, 3, 3, 2, 5, 5, 5,
                               2, 2, 2, 2, 3, 2, 2, 5, 5,
                               5, 5, 5, 2, 3, 3, 2, 2, 2,
                               5, 5, 5, 2, 3, 3, 3, 3, 3]),
  ]
  return {"train": train, "test": test}
