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


def generate(width=None, height=None, wide=None, tall=None, brow=None,
             bcol=None, rows=None, cols=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the grid.
    height: The height of the grid.
    wide: The width of the box.
    tall: The height of the box.
    brow: The row of the box.
    bcol: The column of the box.
    rows: The rows of the pixels.
    cols: The cols of the pixels.
  """

  if width is None:
    width, height = common.randint(8, 13), common.randint(8, 13)
    wide, tall = common.randint(6, width - 2), common.randint(6, height - 2)
    brow = common.randint(1, height - tall - 1)
    bcol = common.randint(1, width - wide - 1)
    while True:
      rows, cols = [], []
      for row in range(1, tall - 3):
        for col in range(1, wide - 3):
          if common.randint(0, 2) == 0:
            rows.append(row)
            cols.append(col)
      if len(rows) > 1 and len(rows) < (tall - 4) * (wide - 4): break

  grid, output = common.grids(width, height)
  common.hollow_rect(grid, wide, tall, brow, bcol, 2)
  common.hollow_rect(output, wide, tall, brow, bcol, 2)
  for row, col in zip(rows, cols):
    grid[brow + 1 + row][bcol + 1 + col] = 5
    output[brow + 1 + row][bcol + 1 + col] = 5
  for row in range(brow + 1, brow + tall - 1):
    rowsum = sum([grid[row][col] for col in range(bcol + 1, bcol + wide - 1)])
    if rowsum: break
    for col in range(bcol + 1, bcol + wide - 1):
      output[row][col] = 2
  for row in range(brow + tall - 2, brow, -1):
    rowsum = sum([grid[row][col] for col in range(bcol + 1, bcol + wide - 1)])
    if rowsum: break
    for col in range(bcol + 1, bcol + wide - 1):
      output[row][col] = 2
  for col in range(bcol + 1, bcol + wide - 1):
    colsum = sum([grid[row][col] for row in range(brow + 1, brow + tall - 1)])
    if colsum: break
    for row in range(brow + 1, brow + tall - 1):
      output[row][col] = 2
  for col in range(bcol + wide - 2, bcol, -1):
    colsum = sum([grid[row][col] for row in range(brow + 1, brow + tall - 1)])
    if colsum: break
    for row in range(brow + 1, brow + tall - 1):
      output[row][col] = 2
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=11, height=12, wide=8, tall=8, brow=1, bcol=1, rows=[2, 3],
               cols=[1, 2]),
      generate(width=11, height=8, wide=8, tall=6, brow=1, bcol=1,
               rows=[1, 1, 2], cols=[1, 4, 3]),
      generate(width=12, height=12, wide=10, tall=8, brow=1, bcol=1,
               rows=[2, 3, 4, 4], cols=[2, 4, 2, 5]),
  ]
  test = [
      generate(width=12, height=13, wide=9, tall=9, brow=1, bcol=2,
               rows=[1, 2, 3, 4], cols=[1, 4, 3, 2]),
  ]
  return {"train": train, "test": test}
