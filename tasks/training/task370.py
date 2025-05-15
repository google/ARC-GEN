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


def generate(width=None, height=None, rows=None, cols=None, bgcolor=None,
             color=None, rdiff=None, cdiff=None, brow=None, bcol=None,
             prow=None, pcol=None, flip=None, xpose=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the input grid
    height: the height of the input grid
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    bgcolor: a digit representing the background color
    color: a digit representing the foreground color
    rdiff: the row delta to add for each iteration of the sprite
    cdiff: the column delta to add for each iteration of the sprite
    brow: the vertical coordinate of the origin sprite
    bcol: the horizontal coordinate of the origin sprite
    prow: the vertical coordinate of the pixel hint
    pcol: the horizontal coordinate of the pixel hint
    flip: whether to flip the sprite
    xpose: whether to transpose the sprite
  """
  if width is None:
    width, height = common.randint(10, 20), common.randint(10, 20)
    length = common.randint(3, 4)
    xrows, xcols = common.conway_sprite(length, length, length * length)
    xrows.append(0)
    xcols.append(0)
    rows, cols = [], []
    for row, col in zip(xrows, xcols):
      rows.append(row)
      cols.append(col)
      rows.append(row)
      cols.append(length - col - 1)
      rows.append(length - row - 1)
      cols.append(col)
      rows.append(length - row - 1)
      cols.append(length - col - 1)
    brow = common.randint(length, height // 2)
    bcol = common.randint(length, width // 2)
    rdiff, cdiff = length, length
    prow, pcol = brow + length, bcol + length
    color = common.random_color()
    bgcolor = common.random_color(exclude=[color])
    flip, xpose = common.randint(0, 1), common.randint(0, 1)

  grid, output = common.grids(width, height, bgcolor)
  for row, col in zip(rows, cols):
    grid[brow + row][bcol + col] = common.black()
    output[brow + row][bcol + col] = common.black()
  grid[prow][pcol] = color
  for _ in range(width + height):
    brow, bcol = brow + rdiff, bcol + cdiff
    for row, col in zip(rows, cols):
      common.draw(output, brow + row, bcol + col, color)
  if flip: grid, output = grid[::-1], output[::-1]
  if xpose: grid, output = common.transpose(grid), common.transpose(output)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=14, height=12, rows=[0, 1, 1, 2], cols=[1, 0, 2, 1],
               bgcolor=8, color=2, rdiff=2, cdiff=2, brow=3, bcol=3, prow=5,
               pcol=6, flip=0, xpose=0),
      generate(width=15, height=13, rows=[0, 1, 1, 1, 2], cols=[1, 0, 1, 2, 1],
               bgcolor=1, color=3, rdiff=2, cdiff=-2, brow=5, bcol=5, prow=7,
               pcol=4, flip=0, xpose=0),
      generate(width=16, height=12,
               rows=[0, 0, 0, 0, 1, 1, 1, 1, 2, 3, 3, 3, 3, 4, 4, 4, 4],
               cols=[0, 1, 3, 4, 0, 1, 3, 4, 2, 0, 1, 3, 4, 0, 1, 3, 4],
               bgcolor=4, color=8, rdiff=-5, cdiff=5, brow=5, bcol=6, prow=4,
               pcol=11, flip=0, xpose=0),
  ]
  test = [
      generate(width=16, height=18, rows=[0, 0, 1, 2, 2], cols=[0, 2, 1, 0, 2],
               bgcolor=3, color=6, rdiff=-3, cdiff=-3, brow=6, bcol=4, prow=5,
               pcol=3, flip=0, xpose=0),
  ]
  return {"train": train, "test": test}
