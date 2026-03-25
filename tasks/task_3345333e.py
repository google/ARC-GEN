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


def generate(rows=None, cols=None, srow=None, scol=None, brow=None, bcol=None,
             wide=None, tall=None, colors=None, off=None, flip=None, size=16):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    srow: the row where the sprite is placed
    scol: the column where the sprite is placed
    brow: the row where the box is placed
    bcol: the column where the box is placed
    wide: the width of the box
    tall: the height of the box
    colors: a list of two colors, one for the sprite and one for the box
    off: an offset to make the sprite length odd or even
    flip: whether to flip the sprite horizontally
    size: the width and height of the (square) grid
  """
  if rows is None:
    pixels = common.continuous_creature(common.randint(8, 24), 4, 8)
    rows, cols = zip(*pixels)
    off, flip = common.randint(0, 1), common.randint(0, 1)
    srow, scol = common.randint(2, 5), common.randint(6, 10)
    brow, bcol = srow + common.randint(1, 2), scol + common.randint(1, 2) - off
    wide, tall = 4, common.randint(3, 5)
    colors = common.random_colors(2)

  grid, output = common.grids(size, size)
  for r, c in zip(rows, cols):
    for bitmap in [grid, output]:
      bitmap[srow + r][scol - c - off] = bitmap[srow + r][scol + c] = colors[0]
  for r in range(brow, brow + tall):
    for c in range(bcol, bcol + wide):
      grid[r][c] = colors[1]
  if flip: grid, output = common.flip_horiz(grid), common.flip_horiz(output)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[0, 0, 1, 1, 2, 2, 3, 4, 5, 5, 6, 7, 7, 8],
               cols=[1, 2, 1, 2, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0],
               srow=2, scol=6, brow=3, bcol=6, wide=4, tall=3, colors=[6, 1],
               off=1, flip=0),
      generate(rows=[0, 1, 1, 1, 2, 2, 2, 2, 3, 3, 4, 5, 5, 5, 6, 6, 6, 7, 7],
               cols=[1, 0, 1, 2, 0, 1, 2, 3, 0, 2, 2, 0, 1, 2, 0, 2, 3, 2, 3],
               srow=3, scol=11, brow=4, bcol=12, wide=4, tall=4, colors=[2, 3],
               off=1, flip=1),
  ]
  test = [
      generate(rows=[0, 1, 1, 1, 2, 2, 3, 3, 3, 3, 3, 4, 5, 5, 5, 5, 5, 6, 6, 6,
                     7],
               cols=[2, 0, 1, 3, 3, 4, 0, 1, 2, 3, 4, 0, 0, 1, 2, 3, 4, 0, 2, 3,
                     2],
               srow=5, scol=6, brow=6, bcol=8, wide=4, tall=5, colors=[5, 8],
               off=0, flip=1),
  ]
  return {"train": train, "test": test}
