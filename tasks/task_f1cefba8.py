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


def generate(width=None, height=None, rows=None, cols=None, brow=None,
             bcol=None, wide=None, tall=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the input grid
    height: the height of the input grid
    rows: a list of vertical coordinates where barnacles should be placed
    cols: a list of horizontal coordinates where barnacles should be placed
    brow: the row where the box should be placed
    bcol: the column where the box should be placed
    wide: the width of the box
    tall: the height of the box
    colors: a pair of digits representing the colors to use
  """
  if width is None:
    wide, tall = common.randint(8, 16), common.randint(8, 16)
    width, height = wide + common.randint(4, 8), tall + common.randint(4, 8)
    brow = common.randint(1, height - tall - 1)
    bcol = common.randint(1, width - wide - 1)
    rows, cols = [], []
    for _ in range(common.randint(2, 3)):  # Barnacles.
      if common.randint(0, 1):  # Top or bottom
        rows.append(-1 if common.randint(0, 1) else tall - 4)
        cols.append(common.randint(0, wide - 5))
      else:  # Left or right
        rows.append(common.randint(0, tall - 5))
        cols.append(-1 if common.randint(0, 1) else wide - 4)
    colors = common.random_colors(2)

  grid, output = common.grids(width, height)
  # First, draw the outside stripes in the output grid.
  for row in range(height):
    for col in range(width):
      if row >= brow + 2 and row < brow + tall - 2:
        if row - brow - 2 in rows: output[row][col] = colors[1]
      if col >= bcol + 2 and col < bcol + wide - 2:
        if col - bcol - 2 in cols: output[row][col] = colors[1]
  # Second, draw the outer squares.
  for row in range(tall):
    for col in range(wide):
      grid[brow + row][bcol + col] = colors[0]
      output[brow + row][bcol + col] = colors[0]
  # Third, draw the inner squares (adding the barnacles).
  for row in range(2, tall - 2):
    for col in range(2, wide - 2):
      color = colors[1]
      grid[brow + row][bcol + col] = color
      if row >= 2 and row < tall - 2 and row - 2 in rows: color = colors[0]
      if col >= 2 and col < wide - 2 and col - 2 in cols: color = colors[0]
      output[brow + row][bcol + col] = color
  for row, col in zip(rows, cols):
    grid[brow + 2 + row][bcol + 2 + col] = colors[1]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=13, height=19, rows=[-1, 9, 2], cols=[4, 1, 7], brow=2,
               bcol=1, wide=11, tall=13, colors=[8, 2]),
      generate(width=17, height=15, rows=[-1, 1, 4], cols=[2, 8, 4], brow=4,
               bcol=2, wide=12, tall=8, colors=[1, 4]),
      generate(width=18, height=16, rows=[-1, 3], cols=[5, -1], brow=3,
               bcol=4, wide=12, tall=12, colors=[2, 3]),
  ]
  test = [
      generate(width=18, height=19, rows=[-1, -1, 4], cols=[3, 7, -1], brow=3,
               bcol=1, wide=14, tall=13, colors=[1, 8]),
  ]
  return {"train": train, "test": test}
