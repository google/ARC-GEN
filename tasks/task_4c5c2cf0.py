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


def generate(size=None, rows=None, cols=None, rowoff=None, coloff=None,
             color=None, legcolor=None, flip_horiz=None, flip_vert=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: the width and height of the (square) grid
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    rowoff: a vertical offset for the body
    coloff: a horizontal offset for the body
    color: a digit representing a color to be used for the body
    legcolor: a digit representing a color to be used for the legs
    flip_horiz: whether to flip the body horizontally
    flip_vert: whether to flip the body vertically
  """
  if rows is None:
    size = common.randint(12, 15)
    width = common.randint(4, size // 2 - 2)
    height = common.randint(4, size // 2 - 2)
    while True:
      rows, cols = common.conway_sprite(width, height, width * height)
      if common.diagonally_connected(list(zip(rows, cols))): break
    rowoff = common.randint(height, size - height - 4)
    coloff = common.randint(width, size - width - 4)
    color = common.random_color()
    legcolor = common.random_color(exclude=[color])
    flip_horiz, flip_vert = common.randint(0, 1), common.randint(0, 1)

  grid, output = common.grids(size, size)
  for r, c in zip(rows, cols):
    output[rowoff - r][coloff - c] = grid[rowoff - r][coloff - c] = legcolor
    output[rowoff - r][coloff + 2 + c] = legcolor
    output[rowoff + 2 + r][coloff - c] = legcolor
    output[rowoff + 2 + r][coloff + 2 + c] = legcolor
  for dr, dc in ([0, 0], [0, 2], [1, 1], [2, 0], [2, 2]):
    output[rowoff + dr][coloff + dc] = grid[rowoff + dr][coloff + dc] = color
  if flip_horiz:
    grid, output = common.flip_horiz(grid), common.flip_horiz(output)
  if flip_vert:
    grid, output = grid[::-1], output[::-1]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=14, rows=[0, 1, 1, 2, 2, 3, 3, 3, 4, 4],
               cols=[3, 1, 2, 0, 1, 0, 2, 3, 0, 3], rowoff=7, coloff=6, color=4,
               legcolor=2, flip_horiz=0, flip_vert=0),
      generate(size=14, rows=[1, 1, 1, 2, 2, 2, 3],
               cols=[0, 1, 2, 1, 2, 3, 2], rowoff=6, coloff=7, color=3,
               legcolor=8, flip_horiz=1, flip_vert=0),
      generate(size=12, rows=[1, 1, 2, 2, 3], cols=[1, 2, 1, 3, 2], rowoff=3,
               coloff=4, color=8, legcolor=1, flip_horiz=0, flip_vert=1),
  ]
  test = [
      generate(size=15, rows=[0, 1, 1, 1, 2, 3, 3, 4, 5],
               cols=[2, 0, 1, 3, 1, 1, 2, 0, 0], rowoff=6, coloff=7, color=7,
               legcolor=4, flip_horiz=1, flip_vert=1),
  ]
  return {"train": train, "test": test}
