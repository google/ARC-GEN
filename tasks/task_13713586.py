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


def generate(width=None, height=None, rows=None, cols=None, wides=None,
             colors=None, flip=None, xpose=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the input grid.
    height: The height of the input grid.
    rows: The rows of the lines.
    cols: The cols of the lines.
    wides: The widths of the lines.
    colors: The colors of the lines.
    flip: Whether to flip the grid.
    xpose: Whether to transpose the grid.
  """

  if width is None:
    width = common.randint(15, 18)
    height = width + common.randint(0, 2) - 1
    wide, wides = common.randint(4, 9), []
    row, rows = common.randint(2, 3), []
    while row + 4 < height and wide >= 2:
      rows.append(row)
      wides.append(wide)
      row += common.randint(2, 5)
      wide = common.randint(2, wide)
    while True:
      cols = [common.randint(0, width - wide) for wide in wides]
      if len(set(cols)) == len(wides): break  # Don't want any to line up.
    colors = common.random_colors(len(wides), exclude=[5])
    flip, xpose = common.randint(0, 1), common.randint(0, 1)

  grid, output = common.grids(width, height)
  for row, col, wide, color in zip(rows, cols, wides, colors):
    for c in range(col, col + wide):
      grid[row][c] = color
    common.rect(output, wide, height - row, row, col, color)
  for col in range(width):
    output[height - 1][col] = grid[height - 1][col] = 5
  if flip:
    grid, output = common.flip(grid), common.flip(output)
  if xpose:
    grid, output = common.transpose(grid), common.transpose(output)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=16, height=17, rows=[2, 6, 11], cols=[7, 4, 1],
               wides=[4, 4, 2], colors=[7, 3, 2], flip=False, xpose=True),
      generate(width=15, height=16, rows=[3, 6, 11], cols=[6, 0, 7],
               wides=[5, 4, 3], colors=[4, 8, 3], flip=False, xpose=False),
      generate(width=17, height=17, rows=[3, 7, 10], cols=[5, 1, 10],
               wides=[8, 6, 2], colors=[6, 3, 2], flip=True, xpose=True),
  ]
  test = [
      generate(width=18, height=19, rows=[3, 7, 11, 13], cols=[2, 8, 0, 14],
               wides=[9, 5, 4, 3], colors=[3, 2, 4, 8], flip=True, xpose=False),
  ]
  return {"train": train, "test": test}
