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


def generate(size=None, rows=None, cols=None, bgcolor=None, fgcolor=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: the width and height of the (square) input grid
    rows: a list of vertical coordinates where lines should be placed
    cols: a list of horizontal coordinates where lines should be placed
    bgcolor: the background color of the grid
    fgcolor: the foreground color of the grid
  """

  if size is None:
    size = common.randint(10, 30)
    row, rows = common.randint(0, size // 2), []
    while row < size:
      rows.append(row)
      row += common.randint(0, size // 2)
    col, cols = common.randint(2, size // 2), []
    while col < size:
      cols.append(col)
      col += common.randint(2, size // 2)
    colors = common.random_colors(2)
    bgcolor, fgcolor = colors[0], colors[1]

  width, height = len(cols) + 1, len(rows) + 1
  if 0 in rows: height -= 1
  if size - 1 in rows: height -= 1
  if 0 in cols: width -= 1
  if size - 1 in cols: width -= 1
  grid = common.grid(size, size, bgcolor)
  output = common.grid(width, height, bgcolor)
  for row in rows:
    for c in range(size):
      grid[row][c] = fgcolor
  for col in cols:
    for r in range(size):
      grid[r][col] = fgcolor
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=27, rows=[9, 14, 19, 24], cols=[6, 16, 19, 25], bgcolor=5,
               fgcolor=8),
      generate(size=21, rows=[10, 13], cols=[3, 8, 18], bgcolor=5, fgcolor=3),
      generate(size=10, rows=[5], cols=[0, 2, 8], bgcolor=1, fgcolor=4),
  ]
  test = [
      generate(size=16, rows=[6, 14], cols=[2, 4, 6, 9], bgcolor=1, fgcolor=3),
  ]
  return {"train": train, "test": test}
