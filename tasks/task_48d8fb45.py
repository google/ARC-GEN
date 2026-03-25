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


def generate(sprites=None, rows=None, cols=None, minirows=None, minicols=None,
             color=None, size=10, minisize=3):
  """Returns input and output grids according to the given parameters.

  Args:
    sprites: a list of digits representing sprite indices
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    minirows: a list of vertical coordinates where sprites should be placed
    minicols: a list of horizontal coordinates where sprites should be placed
    color: a digit representing a color to be used
    size: the width and height of the (square) grid
    minisize: the width and height of the (square) grid for sprites
  """
  if rows is None:
    minirows, minicols = [], []
    for _ in range(4):
      row, col = common.randint(1, size - 3), common.randint(0, size - 3)
      overlaps = False
      for r, c in zip(minirows, minicols):
        overlaps = overlaps or (abs(r - row) < 5 and abs(c - col) <= 4)
      if overlaps: continue
      minirows.append(row)
      minicols.append(col)
    sprites, rows, cols = [], [], []
    for sprite in range(len(minirows)):
      while True:
        sprite_rows, sprite_cols = common.conway_sprite()
        sprite_rows, sprite_cols = sprite_rows + [0], sprite_cols + [1]
        if common.diagonally_connected(list(zip(sprite_rows, sprite_cols))):
          break
      rows, cols = rows + sprite_rows, cols + sprite_cols
      sprites.extend([sprite] * len(sprite_rows))
    color = common.random_color(exclude=[common.gray()])

  grid, output = common.grid(size, size), common.grid(minisize, minisize)
  grid[minirows[0] - 1][minicols[0] + 1] = common.gray()
  for sprite, r, c in zip(sprites, rows, cols):
    mr, mc = minirows[sprite], minicols[sprite]
    grid[mr + r][mc + c] = color
    if sprite != 0: continue
    output[r][c] = color
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(sprites=[0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2],
               rows=[0, 1, 1, 1, 2, 2, 0, 0, 1, 1, 2, 0, 0, 1, 1, 1, 2, 2],
               cols=[1, 0, 1, 2, 1, 2, 1, 2, 0, 1, 1, 1, 2, 0, 1, 2, 1, 2],
               minirows=[3, 1, 7], minicols=[2, 7, 5], color=1),
      generate(sprites=[0, 0, 0, 0, 1, 1, 1, 1, 1],
               rows=[0, 0, 1, 2, 0, 1, 1, 2, 2],
               cols=[0, 1, 2, 1, 1, 0, 2, 1, 2],
               minirows=[2, 3], minicols=[6, 1], color=4),
      generate(sprites=[0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
               rows=[0, 0, 1, 1, 2, 0, 0, 1, 1, 2],
               cols=[1, 2, 0, 1, 1, 1, 2, 0, 2, 1],
               minirows=[5, 2], minicols=[6, 1], color=2),
  ]
  test = [
      generate(sprites=[0, 0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2],
               rows=[0, 1, 1, 2, 2, 0, 1, 1, 2, 0, 1, 1, 1, 2, 2],
               cols=[1, 0, 1, 1, 2, 1, 0, 1, 1, 1, 0, 1, 2, 1, 2],
               minirows=[1, 4, 6], minicols=[5, 1, 5], color=3),
  ]
  return {"train": train, "test": test}
