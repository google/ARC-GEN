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


def generate(width=None, height=None, row=None, col=None, wide=None, tall=None,
             dotrow=None, dotcol=None, inner=None, outer=None, xpose=None,
             flip=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the input grid
    height: the height of the input grid
    row: a vertical coordinate where the box starts
    col: a horizontal coordinate where the box starts
    wide: the width of the box
    tall: the height of the box
    dotrow: the vertical coordinate of the dot
    dotcol: the horizontal coordinate of the dot
    inner: the color of the inner box
    outer: the color of the outer box
    xpose: whether to transpose the grid
    flip: whether to flip the grid
  """
  if width is None:
    width, height = common.randint(11, 13), common.randint(11, 13)
    row, col = common.randint(0, 3), common.randint(0, 3)
    wide, tall = common.randint(3, 5), common.randint(3, 5)
    dotrow = row + tall + common.randint(1, height - tall - row - 1)
    dotcol = col + common.randint(0, wide - 1)
    colors = common.random_colors(2, exclude=[common.cyan()])
    inner, outer = colors[0], colors[1]
    xpose, flip = common.randint(0, 1), common.randint(0, 1)

  grid, output = common.grids(width, height)
  for r in range(row, row + tall):
    for c in range(col, col + wide):
      grid[r][c] = outer
  for r in range(row + 1, row + tall - 1):
    for c in range(col + 1, col + wide - 1):
      grid[r][c] = inner
  grid[dotrow][dotcol] = common.cyan()
  for r in range(row, dotrow + 1):
    for c in range(col, col + wide):
      output[r][c] = outer
  for r in range(row + 1, dotrow):
    for c in range(col + 1, col + wide - 1):
      output[r][c] = inner
  if xpose: grid, output = common.transpose(grid), common.transpose(output)
  if flip: grid, output = grid[::-1], output[::-1]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=11, height=11, row=1, col=1, wide=4, tall=4, dotrow=8,
               dotcol=3, inner=1, outer=2, xpose=0, flip=0),
      generate(width=11, height=11, row=1, col=1, wide=4, tall=5, dotrow=10,
               dotcol=2, inner=2, outer=3, xpose=1, flip=0),
      generate(width=13, height=12, row=2, col=1, wide=5, tall=3, dotrow=10,
               dotcol=5, inner=6, outer=1, xpose=1, flip=0),
  ]
  test = [
      generate(width=13, height=13, row=0, col=3, wide=5, tall=4, dotrow=11,
               dotcol=4, inner=4, outer=6, xpose=0, flip=1),
  ]
  return {"train": train, "test": test}
