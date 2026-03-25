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


def generate(width=None, height=None, rows=None, cols=None, boxrow=None,
             boxcol=None, spriterow=None, spritecol=None, magnifier=None,
             color=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the input grid
    height: the height of the input grid
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    boxrow: a vertical coordinate where the box should be placed
    boxcol: a horizontal coordinate where the box should be placed
    spriterow: a vertical coordinate where the sprite should be placed
    spritecol: a horizontal coordinates where the sprite should be placed
    magnifier: a list of vertical coordinates where magnifiers should be placed
    color: a digit representing a color to be used
  """
  if width is None:
    width, height = common.randint(15, 30), common.randint(15, 30)
    while True:
      rows, cols = common.conway_sprite()
      if common.diagonally_connected(list(zip(rows, cols))): break
    while True:
      magnifier = common.randint(1, 4)
      boxrow = common.randint(0, height - 3 * magnifier - 2)
      boxcol = common.randint(0, width - 3 * magnifier - 2)
      spriterow = common.randint(0, height - 3)
      spritecol = common.randint(0, width - 3)
      if spriterow + 3 <= boxrow or boxrow + 3 * magnifier + 2 <= spriterow:
        if spritecol + 3 <= boxcol or boxcol + 3 * magnifier + 2 <= spritecol:
          break
    color = common.random_color(exclude=[common.red()])

  outsize = 3 * magnifier + 2
  grid, output = common.grid(width, height), common.grid(outsize, outsize)
  for r, c in zip(rows, cols):
    grid[spriterow + r][spritecol + c] = color
    for dr in range(magnifier):
      for dc in range(magnifier):
        output[r * magnifier + dr + 1][c * magnifier + dc + 1] = color
  for i in range(outsize):
    for dr, dc in [(0, i), (outsize - 1, i), (i, 0), (i, outsize - 1)]:
      output[dr][dc] = grid[boxrow + dr][boxcol + dc] = common.red()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=21, height=18, rows=[0, 1, 1, 1, 2], cols=[1, 0, 1, 2, 1],
               boxrow=7, boxcol=6, spriterow=2, spritecol=5, magnifier=2,
               color=8),
      generate(width=22, height=19, rows=[0, 0, 1, 2, 2], cols=[1, 2, 0, 1, 2],
               boxrow=2, boxcol=2, spriterow=9, spritecol=10, magnifier=1,
               color=1),
      generate(width=24, height=21, rows=[0, 0, 1, 1, 2], cols=[1, 2, 0, 2, 2],
               boxrow=1, boxcol=2, spriterow=15, spritecol=13, magnifier=3,
               color=4),
  ]
  test = [
      generate(width=26, height=24, rows=[0, 1, 1, 2], cols=[1, 0, 2, 1],
               boxrow=4, boxcol=2, spriterow=4, spritecol=20, magnifier=4,
               color=3),
  ]
  return {"train": train, "test": test}
