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


def generate(sprites=None, rows=None, cols=None, xpose=None, size=9,
             minisize=3):
  """Returns input and output grids according to the given parameters.

  Args:
    sprites: a list of sprite indices for the pixels
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    xpose: whether to transpose the grid (it's an inverted transpose)
    size: the width and height of the (square) grid
    minisize: the width and height of the sprites
  """
  if rows is None:
    sprites, rows, cols = [], [], []
    for sprite in range(2):
      while True:
        sprite_rows, sprite_cols = common.conway_sprite()
        if common.diagonally_connected(list(zip(sprite_rows, sprite_cols))):
          break
      sprites.extend([sprite] * len(sprite_rows))
      rows.extend(sprite_rows)
      cols.extend(sprite_cols)
    xpose = common.randint(0, 1)

  grid, output = common.grids(size, size)
  for sprite, row, col in zip(sprites, rows, cols):
    r, c = row + (4 if sprite else 1), col + (5 if sprite else 0)
    output[r][c] = grid[r][c] = common.yellow()
  for sprite in range(2):
    for row in range(minisize):
      for col in range(minisize):
        r, c = row + (4 if sprite else 1), col + (5 if sprite else 0)
        output[r][c] = common.yellow() if output[r][c] else common.orange()
  if xpose:
    grid = common.transpose_inverted(grid)
    output = common.transpose_inverted(output)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(sprites=[0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1],
               rows=[0, 0, 0, 1, 1, 2, 0, 0, 1, 1, 2, 2],
               cols=[0, 1, 2, 0, 2, 2, 0, 1, 1, 2, 0, 2],
               xpose=0),
      generate(sprites=[0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
               rows=[0, 0, 0, 1, 1, 2, 2, 2, 0, 0, 0, 1, 2],
               cols=[0, 1, 2, 1, 2, 0, 1, 2, 0, 1, 2, 1, 1],
               xpose=0),
  ]
  test = [
      generate(sprites=[0, 0, 0, 0, 0, 1, 1, 1, 1],
               rows=[0, 1, 1, 2, 2, 0, 1, 2, 2],
               cols=[1, 0, 1, 1, 2, 2, 1, 0, 1],
               xpose=1),
  ]
  return {"train": train, "test": test}
