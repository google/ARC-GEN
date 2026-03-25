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


def generate(size=None, quadrant=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: The size of the grid.
    quadrant: The quadrant of the target box.
    colors: The colors of the pixels.
  """

  if size is None:
    size = 2 * common.randint(2, 6) + 1
    half = size // 2
    subset = common.sample([0, 1, 2, 3, 4, 5, 6, 8, 9], 4)
    while True:
      grid = common.grid(size, size, 7)
      for row in range(2):
        for col in range(2):
          for r in range(half):
            for c in range(half):
              if common.randint(0, 1): continue
              grid[row * (half + 1) + r][col * (half + 1) + c] = subset[row * 2 + col]
      colors = common.flatten(grid)
      if len(set(colors)) == 5: break
    quadrant = common.randint(0, 3)
    grid[half][half] = subset[quadrant]
    colors = common.flatten(grid)

  grid, output = common.grids(size, size, 7)
  for i, color in enumerate(colors):
    grid[i // size][i % size] = color
  color = grid[size // 2][size // 2]
  for i in range(size // 2 + 1):
    if quadrant == 0: output[i][i] = color
    if quadrant == 1: output[i][size - i - 1] = color
    if quadrant == 2: output[size - i - 1][i] = color
    if quadrant == 3: output[size - i - 1][size - i - 1] = color
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=11, quadrant=1,
               colors=[7, 3, 7, 3, 7, 7, 7, 0, 7, 7, 0,
                       7, 7, 3, 7, 3, 7, 7, 7, 7, 0, 7,
                       3, 7, 3, 7, 7, 7, 0, 0, 0, 0, 0,
                       7, 3, 7, 3, 7, 7, 7, 0, 7, 0, 7,
                       7, 7, 3, 7, 3, 7, 7, 7, 0, 7, 0,
                       7, 7, 7, 7, 7, 0, 7, 7, 7, 7, 7,
                       2, 2, 7, 2, 7, 7, 7, 7, 7, 9, 7,
                       7, 7, 2, 7, 2, 7, 9, 7, 9, 7, 9,
                       7, 2, 7, 2, 7, 7, 9, 7, 9, 9, 7,
                       7, 7, 7, 2, 7, 7, 7, 7, 9, 7, 9,
                       7, 2, 7, 7, 2, 7, 7, 9, 7, 7, 9]),
      generate(size=7, quadrant=2,
               colors=[0, 7, 0, 7, 4, 7, 7,
                       0, 7, 7, 7, 7, 4, 7,
                       7, 0, 7, 7, 4, 4, 7,
                       7, 7, 7, 5, 7, 7, 7,
                       5, 5, 7, 7, 7, 1, 7,
                       7, 5, 5, 7, 1, 1, 7,
                       7, 7, 5, 7, 1, 7, 7]),
  ]
  test = [
      generate(size=13, quadrant=2,
               colors=[8, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 6, 7,
                       7, 7, 8, 7, 8, 7, 7, 7, 6, 6, 7, 7, 6,
                       7, 8, 7, 8, 7, 8, 7, 7, 7, 6, 7, 7, 7,
                       7, 7, 7, 8, 7, 7, 7, 7, 6, 7, 6, 6, 7,
                       8, 7, 8, 7, 8, 7, 7, 6, 7, 6, 7, 7, 6,
                       7, 8, 7, 7, 7, 8, 7, 6, 6, 6, 7, 6, 7,
                       7, 7, 7, 7, 7, 7, 4, 7, 7, 7, 7, 7, 7,
                       7, 4, 4, 7, 4, 7, 7, 7, 2, 7, 7, 2, 7,
                       4, 7, 7, 7, 7, 7, 7, 7, 7, 2, 2, 7, 7,
                       7, 4, 7, 4, 4, 7, 7, 7, 2, 7, 7, 7, 7,
                       7, 7, 4, 4, 4, 7, 7, 2, 7, 2, 2, 2, 7,
                       7, 4, 7, 7, 7, 7, 7, 7, 7, 2, 7, 7, 2,
                       7, 7, 7, 7, 4, 7, 7, 2, 7, 7, 2, 7, 7]),
  ]
  return {"train": train, "test": test}
