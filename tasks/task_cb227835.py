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


def generate(width=None, height=None, prows=None, pcols=None, flip=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the grid.
    height: The height of the grid.
    prows: The rows of the pixels.
    pcols: The columns of the pixels.
    flip: Whether to flip the grid.
  """

  if width is None:
    width = 12 + common.randint(-2, 2)
    height = 12 + common.randint(-2, 2)
    while True:
      wide, tall = common.randint(3, width - 1), common.randint(3, height - 1)
      if abs(wide - tall) >= 2: break
    brow = common.randint(0, height - tall)
    bcol = common.randint(0, width - wide)
    prows = [brow, brow + tall - 1]
    pcols = [bcol, bcol + wide - 1]
    flip = common.randint(0, 1)

  grid, output = common.grids(width, height)
  row_diff, col_diff = pcols[1] - pcols[0], prows[1] - prows[0]
  if row_diff > col_diff:
    for i in range(row_diff - col_diff + 1):
      output[prows[0]][pcols[0] + i] = 3
      output[prows[1]][pcols[1] - i] = 3
    for i in range(col_diff):
      output[prows[0] + i][pcols[0] + i] = 3
      output[prows[1] - i][pcols[1] - i] = 3
  else:
    for i in range(col_diff - row_diff + 1):
      output[prows[0] + i][pcols[0]] = 3
      output[prows[1] - i][pcols[1]] = 3
    for i in range(row_diff):
      output[prows[0] + i][pcols[0] + i] = 3
      output[prows[1] - i][pcols[1] - i] = 3
  for prow, pcol in zip(prows, pcols):
    output[prow][pcol] = grid[prow][pcol] = 8
  if flip: grid, output = common.flip(grid), common.flip(output)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=14, height=12, prows=[4, 11], pcols=[2, 11], flip=True),
      generate(width=13, height=13, prows=[1, 10], pcols=[2, 8], flip=False),
      generate(width=14, height=11, prows=[2, 4], pcols=[2, 12], flip=True),
  ]
  test = [
      generate(width=14, height=13, prows=[1, 12], pcols=[1, 8], flip=False),
  ]
  return {"train": train, "test": test}
