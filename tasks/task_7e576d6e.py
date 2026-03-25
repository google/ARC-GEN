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


def generate(start_row=None, start_col=None, end_row=None, end_col=None,
             rows=None, cols=None, colors=None, xpose=None):
  """Returns input and output grids according to the given parameters.

  Args:
    start_row: The start row.
    start_col: The start column.
    end_row: The end row.
    end_col: The end column.
    rows: The rows of the lines.
    cols: The columns of the centers.
    colors: The colors of the grid.
    xpose: Whether to transpose the grid.
  """

  def draw():
    grid, output = common.grids(30, 30, colors[0])
    for row in rows:
      for col in range(30):
        output[row][col] = grid[row][col] = colors[1]
    for row, col in zip(rows, cols):
      for c in [-1, 0, 1]:
        output[row][col + c] = grid[row][col + c] = colors[2]
    grid[start_row][start_col] = grid[end_row][end_col] = colors[3]
    output[start_row][start_col] = output[end_row][end_col] = colors[3]
    r, c = start_row, start_col
    last_cdir = 0
    for row, col in zip(rows, cols):
      while r + 1 < row:
        output[r][c] = colors[3]
        r += 1
      cdir = 1 if c < col else -1
      if last_cdir and last_cdir == cdir: return None, None
      last_cdir = cdir
      while c != col:
        output[r][c] = colors[3]
        c += cdir
    while r < end_row:
      output[r][c] = colors[3]
      r += 1
    cdir = 1 if c < end_col else -1
    if last_cdir and last_cdir == cdir: return None, None
    while c != end_col:
      output[r][c] = colors[3]
      c += cdir
    if xpose: grid, output = common.transpose(grid), common.transpose(output)
    return grid, output

  if start_col is None:
    colors = common.random_colors(4)
    start_row, start_col = 1, common.randint(4, 25)
    end_row, end_col = common.randint(25, 28), common.randint(4, 25)
    while True:
      row, rows = 0, []
      while True:
        row += common.randint(3, 8)
        if row + 7 >= 30: break
        rows.append(row)
      if len(rows) not in [3, 4]: continue
      cols = common.sample(list(range(4, 25)), len(rows))
      if start_col in cols or end_col in cols: continue  # Undefined.
      grid, _ = draw()
      if grid: break

  grid, output = draw()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(start_row=1, start_col=10, end_row=27, end_col=15,
               rows=[4, 11, 19], cols=[4, 18, 7], colors=[3, 2, 4, 8],
               xpose=True),
      generate(start_row=1, start_col=18, end_row=26, end_col=24,
               rows=[6, 11, 23], cols=[4, 17, 7], colors=[8, 6, 1, 3],
               xpose=True),
      generate(start_row=1, start_col=8, end_row=27, end_col=12,
               rows=[3, 8, 17, 23], cols=[6, 16, 9, 22], colors=[1, 2, 3, 9],
               xpose=False),
  ]
  test = [
      generate(start_row=1, start_col=4, end_row=28, end_col=10,
               rows=[3, 8, 19, 22], cols=[13, 6, 18, 5], colors=[8, 1, 6, 3],
               xpose=False),
  ]
  return {"train": train, "test": test}
