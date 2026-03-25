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
    legend = common.random_colors(4)
    while True:
      grid = common.grid(10, 10)
      i = 0
      while i < 10 or len(set(common.flatten(grid))) < 5:
        color = common.choice(legend + [0])
        if common.randint(0, 1):
          row = common.randint(0, 7)
          length = common.randint(1, 6)
          col = common.randint(0, 6 - length)
          for c in range(col, col + length):
            grid[1 + row][2 + c] = color
        else:
          col = common.randint(0, 5)
          length = common.randint(1, 8)
          row = common.randint(0, 8 - length)
          for r in range(row, row + length):
            grid[1 + r][2 + col] = color
        i += 1
      if grid[0][2] or grid[1][2] or grid[2][2]: continue
      pixels = []
      for r in range(10):
        for c in range(10):
          if grid[r][c]: pixels.append((r, c))
      if common.connected(pixels): break
    grid[0][0] = legend[0]
    grid[0][1] = legend[1]
    grid[1][0] = legend[2]
    grid[1][1] = legend[3]
    colors = common.flatten(grid)

  grid, output = common.grids(10, 10)
  for i, color in enumerate(colors):
    grid[i // 10][i % 10] = color
    if i in [0, 1, 10, 11]: output[i // 10][i % 10] = color
    else:
      if color == colors[0]: output[i // 10][i % 10] = colors[1]
      elif color == colors[1]: output[i // 10][i % 10] = colors[0]
      elif color == colors[10]: output[i // 10][i % 10] = colors[11]
      elif color == colors[11]: output[i // 10][i % 10] = colors[10]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors=[1, 3, 0, 0, 0, 0, 0, 0, 0, 0,
                       2, 8, 0, 0, 0, 0, 1, 0, 0, 0,
                       0, 0, 0, 0, 1, 1, 1, 0, 0, 0,
                       0, 0, 0, 0, 1, 1, 1, 0, 0, 0,
                       0, 0, 3, 3, 3, 3, 1, 8, 0, 0,
                       0, 0, 3, 3, 2, 0, 8, 8, 0, 0,
                       0, 0, 0, 0, 2, 0, 8, 8, 0, 0,
                       0, 0, 0, 0, 2, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 2, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
      generate(colors=[4, 2, 0, 0, 0, 0, 0, 0, 0, 0,
                       3, 7, 0, 0, 0, 0, 4, 0, 0, 0,
                       0, 0, 0, 0, 0, 3, 4, 4, 0, 0,
                       0, 0, 0, 0, 0, 3, 2, 4, 0, 0,
                       0, 0, 0, 7, 7, 3, 2, 4, 0, 0,
                       0, 0, 0, 7, 3, 3, 2, 0, 0, 0,
                       0, 0, 0, 7, 0, 0, 2, 2, 0, 0,
                       0, 0, 0, 7, 7, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
      generate(colors=[9, 4, 0, 0, 0, 0, 0, 0, 0, 0,
                       7, 6, 0, 0, 0, 9, 9, 0, 0, 0,
                       0, 0, 0, 0, 0, 7, 9, 0, 0, 0,
                       0, 0, 0, 0, 0, 4, 0, 0, 0, 0,
                       0, 0, 0, 0, 7, 4, 0, 0, 0, 0,
                       0, 0, 0, 6, 6, 7, 0, 0, 0, 0,
                       0, 0, 0, 7, 6, 6, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
  ]
  test = [
      generate(colors=[8, 9, 0, 0, 0, 0, 0, 0, 0, 0,
                       2, 4, 0, 0, 0, 9, 9, 0, 0, 0,
                       0, 0, 0, 8, 8, 8, 9, 0, 0, 0,
                       0, 0, 0, 2, 8, 8, 9, 0, 0, 0,
                       0, 0, 0, 2, 4, 2, 0, 0, 0, 0,
                       0, 0, 0, 2, 2, 4, 0, 0, 0, 0,
                       0, 0, 0, 2, 4, 4, 0, 0, 0, 0,
                       0, 0, 0, 9, 4, 4, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 4, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
  ]
  return {"train": train, "test": test}
