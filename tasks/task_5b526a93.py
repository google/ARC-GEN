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


def generate(width=None, height=None, rows=None, cols=None, flip=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the grid.
    height: The height of the grid.
    rows: The rows of the boxes.
    cols: The columns of the boxes.
    flip: Whether to flip the grid.
  """

  if width is None:
    width, height = common.randint(15, 30), common.randint(15, 30)
    rows, cols = [], []
    row, col = common.randint(2, 3), common.randint(2, 3)
    while row <= height - 3:
      rows.append(row)
      row += common.randint(4, 6)
    while col <= width - 3:
      cols.append(col)
      col += common.randint(4, 6)
    flip = common.randint(0, 1)

  grid, output = common.grids(width, height)
  for r, row in enumerate(rows):
    for c, col in enumerate(cols):
      for i in [-1, 0, 1]:
        for j in [-1, 0, 1]:
          if i == 0 and j == 0: continue
          if r == 0 or c == 0:
            output[row + i][col + j] = 1
            grid[row + i][col + j] = 1
          else:
            output[row + i][col + j] = 8
  if flip:
    grid, output = common.flip(grid), common.flip(output)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=16, height=22, rows=[2, 8, 12, 18], cols=[2, 7, 13],
               flip=False),
      generate(width=17, height=19, rows=[2, 9, 14], cols=[3, 7, 13],
               flip=True),
  ]
  test = [
      generate(width=30, height=21, rows=[3, 7, 13, 18],
               cols=[3, 8, 12, 18, 22], flip=True),
  ]
  return {"train": train, "test": test}
