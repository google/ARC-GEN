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


def generate(yrows=None, ycols=None, ytalls=None, brow=None, drow=None,
             dtalls=None, flip=None, xpose=None):
  """Returns input and output grids according to the given parameters.

  Args:
    yrows: the rows of the (vertical) yellow lines.
    ycols: the columns of the yellow lines.
    ytalls: the heights of the yellow lines.
    brow: the row of the blue line.
    drow: the row of the red lines.
    dtalls: the heights of the red lines.
    flip: whether to flip the grid.
    xpose: whether to transpose the grid.
  """

  if yrows is None:
    yrows, ycols, ytalls = [], [], []
    ycol = 0
    while True:
      ycol += common.randint(1, 5)
      wide = common.randint(2, 5)
      if ycol + wide + 1 >= 30: break
      yrow = common.randint(0, 7)
      ytall = min(common.randint(1, 3), yrow + 1)
      for col in range(ycol, ycol + wide):
        yrows.append(yrow)
        ycols.append(col)
        ytalls.append(common.randint(1, ytall))
      ycol += wide
    brow, drow = common.randint(9, 10), common.randint(19, 23)
    dtalls = common.choices([1, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 4, 4, 5], 30)
    flip, xpose = common.randint(0, 1), common.randint(0, 1)

  grid, output = common.grids(30, 30)
  # First, draw yellow/green boxes, along with the yellow/blue lines.
  for yrow, ycol, ytall in zip(yrows, ycols, ytalls):
    for row in range(ytall):
      grid[yrow - row][ycol], output[yrow - row][ycol] = 4, 3
    for row in range(yrow + 1, brow):
      output[row][ycol] = 4
    for row in range(brow, 30):
      output[row][ycol] = 8
  # Second, draw the blue line
  for col in range(30):
    output[brow][col] = grid[brow][col] = 8
  # Third, draw the red shapes
  for col, dtall in enumerate(dtalls):
    for row in range(dtall):
      grid[drow - row][col] = 2
      offset = 29 if col in ycols else drow
      output[offset - row][col] = 2
  if flip: grid, output = common.flip(grid), common.flip(output)
  if xpose: grid, output = common.transpose(grid), common.transpose(output)

  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(yrows=[3, 3, 2, 2, 5, 5, 5, 4], ycols=[4, 5, 11, 12, 18, 19, 20, 25],
               ytalls=[2, 2, 1, 1, 2, 2, 1, 2], brow=9, drow=20,
               dtalls=[1, 2, 3, 2, 1, 1, 3, 2, 4, 3, 1, 2, 3, 2, 1, 2, 1, 1, 2, 3, 3, 1, 1, 2, 1, 2, 1, 2, 2, 1],
               flip=False, xpose=True),
      generate(yrows=[5, 5, 4, 4, 4, 4, 4, 7, 7, 7],
               ycols=[3, 4, 9, 10, 17, 18, 19, 23, 24, 25],
               ytalls=[1, 1, 1, 2, 2, 2, 2, 1, 3, 3], brow=10, drow=21,
               dtalls=[2, 1, 1, 2, 2, 1, 1, 2, 1, 2, 1, 1, 2, 3, 1, 1, 1, 2, 1, 2, 1, 1, 3, 3, 2, 1, 1, 2, 1, 1],
               flip=False, xpose=False),
      generate(yrows=[2, 2, 2, 2, 2, 5, 5, 5, 5, 4, 4],
               ycols=[6, 7, 8, 9, 10, 16, 17, 18, 19, 25, 26],
               ytalls=[1, 1, 1, 1, 1, 2, 2, 2, 2, 1, 1], brow=9, drow=22,
               dtalls=[1, 1, 2, 2, 1, 2, 2, 3, 4, 4, 2, 1, 2, 1, 2, 4, 3, 1, 2, 1, 2, 2, 1, 2, 1, 2, 2, 1, 1, 1],
               flip=False, xpose=False),
  ]
  test = [
      generate(yrows=[4, 4, 4, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0, 4],
               ycols=[1, 2, 3, 10, 11, 12, 13, 14, 15, 20, 21, 22, 23, 26, 27],
               ytalls=[2, 2, 3, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1], brow=10, drow=19,
               dtalls=[1, 3, 2, 2, 3, 2, 5, 4, 1, 1, 3, 2, 1, 3, 4, 2, 1, 2, 1, 2, 3, 5, 2, 3, 4, 2, 2, 3, 3, 1],
               flip=True, xpose=True),
  ]
  return {"train": train, "test": test}
