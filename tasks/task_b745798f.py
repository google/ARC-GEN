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


def generate(size=None, rows=None, cols=None, colors=None, bgcolor=8):
  """Returns input and output grids according to the given parameters.

  Args:
    size: The size of the grid.
    rows: The rows of the boxes.
    cols: The columns of the boxes.
    colors: The colors of the boxes.
    bgcolor: The background color of the grid.
  """

  def draw(grid):
    for i in range(4):
      row, col, color = rows[i], cols[i], colors[i]
      for r in range(2):
        for c in range(2):
          if r * 2 + c == 3 - i: continue
          if grid[row + r][col + c] != bgcolor: return False
          grid[row + r][col + c] = color
    return True

  if size is None:
    size = 2 * common.randint(2, 7) + 1
    if common.randint(0, 1):  # rectangle -- colors can be anything.
      colors = [common.random_color() for _ in range(4)]
      colors = [color if color != bgcolor else 0 for color in colors]
      width, height = common.randint(5, size), common.randint(5, size)
      row = common.randint(0, size - height)
      col = common.randint(0, size - width)
      rows = [row, row, row + height - 2, row + height - 2]
      cols = [col, col + width - 2, col, col + width - 2]
    else:  # scattered -- colors must be different.
      colors = common.sample(range(1, 10), 4)
      colors = [color if color != bgcolor else 0 for color in colors]
      while True:
        rows = [common.randint(0, size - 2) for _ in range(4)]
        cols = [common.randint(0, size - 2) for _ in range(4)]
        grid = common.grid(size, size, bgcolor)
        if draw(grid): break

  grid, output = common.grids(size, size, bgcolor)
  draw(grid)
  for row in range(size):
    for col in range(size):
      if row not in [0, size - 1] and col not in [0, size - 1]: continue
      if row * 2 + 1 == size or col * 2 + 1 == size: continue
      r = 0 if row * 2 < size else 1
      c = 0 if col * 2 < size else 1
      output[row][col] = colors[r * 2 + c]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=11, rows=[0, 0, 3, 3], cols=[2, 9, 2, 9], colors=[2, 5, 1, 5]),
      generate(size=9, rows=[2, 2, 5, 5], cols=[2, 6, 2, 6], colors=[3, 2, 7, 0]),
      generate(size=5, rows=[3, 2, 0, 3], cols=[3, 0, 3, 1], colors=[4, 2, 0, 7]),
  ]
  test = [
      generate(size=15, rows=[13, 13, 13, 11], cols=[12, 9, 5, 9], colors=[9, 3, 6, 2]),
  ]
  return {"train": train, "test": test}
