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
    grid, output = common.grids(10, 10)
    for i, color in enumerate(colors):
      output[i // 10][i % 10] = grid[i // 10][i % 10] = color
    for size in range(9, 1, -1):
      coords = []
      for row in range(11 - size):
        for col in range(11 - size):
          good = True
          for r in range(row, row + size):
            for c in range(col, col + size):
              if output[r][c]: good = False
          if good: coords.append((row, col))
      for row, col in coords:
        for r in range(row, row + size):
          for c in range(col, col + size):
            if output[r][c]: return None, None
            output[r][c] = 1
    return grid, output

  if colors is None:
    num_boxes = common.randint(3, 5)
    while True:
      sizes = [2 if common.randint(0, 2) else 3 for _ in range(num_boxes)]
      brows = [common.randint(0, 10 - size) for size in sizes]
      bcols = [common.randint(0, 10 - size) for size in sizes]
      if common.overlaps(brows, bcols, sizes, sizes): continue
      grid = common.grid(10, 10)
      for row in range(10):
        for col in range(10):
          grid[row][col] = 5 if common.randint(0, 2) else 0
      for br, bc, size in zip(brows, bcols, sizes):
        for r in range(br, br + size):
          for c in range(bc, bc + size):
            grid[r][c] = 0
      colors = common.flatten(grid)
      grid, _ = draw()
      if grid: break

  grid, output = draw()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors=[0, 5, 0, 0, 5, 0, 0, 0, 0, 0,
                       5, 5, 0, 0, 0, 5, 5, 0, 5, 0,
                       0, 0, 0, 5, 5, 0, 0, 5, 5, 5,
                       0, 0, 5, 0, 5, 5, 0, 0, 5, 0,
                       0, 5, 0, 0, 0, 0, 0, 0, 5, 0,
                       5, 0, 5, 0, 0, 5, 5, 5, 0, 5,
                       0, 0, 0, 5, 0, 5, 5, 0, 5, 0,
                       0, 0, 5, 0, 5, 5, 5, 0, 0, 0,
                       5, 0, 5, 5, 0, 5, 5, 0, 5, 0,
                       0, 0, 0, 0, 0, 0, 0, 5, 0, 0]),
      generate(colors=[5, 5, 0, 0, 0, 0, 0, 5, 0, 0,
                       0, 0, 5, 5, 0, 0, 0, 0, 5, 5,
                       5, 5, 0, 5, 0, 0, 0, 0, 5, 0,
                       0, 0, 0, 0, 5, 5, 5, 5, 0, 5,
                       0, 5, 0, 5, 0, 5, 5, 0, 5, 0,
                       5, 0, 0, 0, 0, 5, 0, 0, 5, 5,
                       5, 5, 5, 0, 5, 0, 0, 0, 0, 5,
                       0, 5, 0, 0, 0, 0, 5, 5, 5, 0,
                       5, 0, 0, 0, 0, 5, 0, 0, 5, 5,
                       5, 0, 0, 0, 0, 0, 5, 5, 0, 0]),
      generate(colors=[0, 0, 5, 0, 0, 0, 0, 5, 0, 5,
                       0, 5, 0, 0, 0, 5, 0, 0, 0, 5,
                       0, 0, 5, 0, 5, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 5, 0, 0, 0, 0, 0,
                       0, 5, 5, 0, 0, 5, 5, 5, 0, 5,
                       5, 0, 0, 5, 0, 5, 0, 0, 0, 0,
                       5, 5, 5, 5, 0, 5, 5, 5, 0, 0,
                       0, 0, 0, 5, 0, 0, 0, 0, 5, 0,
                       0, 0, 0, 0, 5, 5, 5, 5, 5, 5,
                       0, 0, 0, 0, 0, 5, 0, 0, 5, 0]),
  ]
  test = [
      generate(colors=[5, 0, 0, 0, 5, 0, 5, 0, 5, 0,
                       5, 0, 0, 5, 0, 5, 5, 0, 0, 0,
                       5, 5, 0, 5, 5, 0, 0, 5, 5, 0,
                       5, 0, 0, 0, 0, 0, 0, 5, 0, 0,
                       5, 0, 0, 0, 5, 5, 0, 0, 0, 5,
                       0, 0, 0, 0, 0, 0, 5, 5, 0, 0,
                       0, 0, 5, 5, 0, 0, 5, 5, 0, 0,
                       5, 0, 5, 0, 5, 0, 5, 0, 0, 5,
                       0, 5, 5, 0, 5, 0, 0, 5, 5, 5,
                       0, 0, 0, 5, 5, 5, 0, 0, 0, 0]),
  ]
  return {"train": train, "test": test}
