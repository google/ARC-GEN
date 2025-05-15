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


def generate(
    width=None,
    height=None,
    spriterow=None,
    spritecol=None,
    brow=None,
    bcol=None,
    rows=None,
    cols=None,
    colors=None,
):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the input grid
    height: the height of the input grid
    spriterow: the row of the sprite in the input grid
    spritecol: the column of the sprite in the input grid
    brow: the row of the box
    bcol: the column of the box
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    colors: a list of digits representing the colors to be used
  """
  if width is None:
    width, height = common.randint(14, 16), common.randint(14, 16)
    length = common.randint(3, 5)
    colors = common.random_colors(4, exclude=[common.cyan()])
    rows, cols = common.conway_sprite(length, length, 2 * length)
    while True:
      spriterow = common.randint(0, height - length)
      spritecol = common.randint(0, width - length)
      brow = common.randint(0, height - length - 2)
      bcol = common.randint(0, width - length - 2)
      if abs(brow - spriterow) >= length + 2: break
      if abs(bcol - spritecol) >= length + 2: break

  length = max(rows) + 1
  grid = common.grid(width, height)
  output = common.grid(length + 2, length + 2)
  for r, c in zip(rows, cols):
    output[r + 1][c + 1] = grid[spriterow + r][spritecol + c] = common.cyan()
  p = length + 1  # Shorthand
  for i in range(1, p):
    output[0][i] = grid[brow][bcol + i] = colors[0]
    output[i][p] = grid[brow + i][bcol + p] = colors[1]
    output[p][i] = grid[brow + p][bcol + i] = colors[2]
    output[i][0] = grid[brow + i][bcol] = colors[3]
  for r in range(length):
    for c in range(length):
      if not output[r + 1][c + 1]:
        continue
      diag0, diag1, color = r - c, length - 1 - r - c, common.cyan()
      if diag0 < 0 and diag1 > 0: color = colors[0]
      if diag0 < 0 and diag1 < 0: color = colors[1]
      if diag0 > 0 and diag1 < 0: color = colors[2]
      if diag0 > 0 and diag1 > 0: color = colors[3]
      output[r + 1][c + 1] = color
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=16, height=15, spriterow=1, spritecol=1, brow=7, bcol=6,
               rows=[0, 0, 1, 1, 2, 2, 2, 2, 3, 3],
               cols=[0, 3, 1, 3, 0, 1, 2, 3, 1, 3], colors=[4, 1, 3, 2]),
      generate(width=16, height=14, spriterow=2, spritecol=8, brow=6, bcol=1,
               rows=[0, 1, 1, 1, 2, 2],
               cols=[1, 0, 1, 2, 1, 2], colors=[3, 4, 2, 6]),
      generate(width=15, height=15, spriterow=9, spritecol=6, brow=1, bcol=2,
               rows=[0, 0, 0, 1, 1, 2, 2, 3, 3, 3],
               cols=[0, 1, 3, 1, 2, 1, 3, 0, 1, 3], colors=[7, 6, 1, 4]),
  ]
  test = [
      generate(width=16, height=16, spriterow=9, spritecol=2, brow=0, bcol=5,
               rows=[0, 0, 0, 0, 1, 1, 1, 2, 2, 2, 2, 3, 4, 4, 4, 4],
               cols=[0, 1, 3, 4, 0, 2, 3, 1, 2, 3, 4, 2, 0, 1, 3, 4],
               colors=[1, 4, 3, 2]),
  ]
  return {"train": train, "test": test}
