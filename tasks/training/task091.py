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


def generate(width=None, height=None, rows=None, cols=None, zoom_width=None,
             zoom_height=None, row=None, col=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of one grid half
    height: the height of the grid
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    zoom_width: the width of the zoom
    zoom_height: the height of the zoom
    row: the row where the zoom starts
    col: the column where the zoom starts
  """
  if width is None:
    width, height = common.randint(9, 15), common.randint(9, 15)
    rows, cols = [], []
    for r in range(height):
      for c in range(width):
        if common.randint(0, 9) != 0: continue
        rows.append(r)
        cols.append(c)
    zoom_width = common.randint(3, width - 1)
    zoom_height = common.randint(3, height - 1)
    row = common.randint(0, height - zoom_height)
    col = common.randint(0, width - zoom_width)

  grid = common.grid(width, height)
  output = common.grid(zoom_width, zoom_height)
  for r, c in zip(rows, cols):
    grid[r][c] = common.cyan()
    if r < row or r >= row + zoom_height: continue
    if c < col or c >= col + zoom_width: continue
    output[r - row][c - col] = common.cyan()
  # Tips of the glowsticks in the input
  grid[row][col] = common.cyan()
  grid[row + zoom_height - 1][col] = common.cyan()
  grid[row][col + zoom_width - 1] = common.cyan()
  grid[row + zoom_height - 1][col + zoom_width - 1] = common.cyan()
  # Tips of the glowsticks in the output
  output[0][0] = common.cyan()
  output[zoom_height - 1][0] = common.cyan()
  output[0][zoom_width - 1] = common.cyan()
  output[zoom_height - 1][zoom_width - 1] = common.cyan()
  # Grey center of the glowsticks in the input and output
  for r in range(row + 1, row + zoom_height - 1):
    grid[r][col] = grid[r][col + zoom_width - 1] = common.gray()
    output[r - row][0] = output[r - row][zoom_width - 1] = common.gray()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=9, height=9, rows=[1, 3, 3, 7, 7, 8],
               cols=[8, 3, 7, 3, 7, 1], zoom_width=5, zoom_height=5, row=1,
               col=1),
      generate(width=11, height=9,
               rows=[0, 1, 1, 1, 2, 2, 4, 5, 5, 7, 8, 8, 8],
               cols=[1, 2, 6, 10, 9, 10, 0, 5, 6, 4, 1, 8, 9], zoom_width=7,
               zoom_height=5, row=3, col=2),
      generate(width=13, height=11,
               rows=[0, 0, 3, 4, 4, 5, 6, 6, 7, 8, 9, 9, 9, 10],
               cols=[9, 10, 9, 2, 5, 8, 2, 5, 10, 10, 2, 3, 7, 8], zoom_width=5,
               zoom_height=6, row=2, col=3),
  ]
  test = [
      generate(width=13, height=14,
               rows=[0, 2, 4, 4, 7, 7, 8, 8, 8, 9, 10, 10, 10, 11, 13],
               cols=[0, 8, 12, 1, 6, 9, 2, 4, 12, 5, 1, 10, 12, 7, 12],
               zoom_width=4, zoom_height=10, row=3, col=0),
  ]
  return {"train": train, "test": test}
