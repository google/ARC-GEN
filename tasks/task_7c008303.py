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


def generate(rows=None, cols=None, colors=None, flip_horiz=None, flip_vert=None,
             size=6):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    colors: a list of four digits representing the colors to be used
    flip_horiz: whether to flip the grid horizontally
    flip_vert: whether to flip the grid vertically
    size: the width and height of the (square) grid
  """
  if rows is None:
    pixels = common.random_pixels(size, size)
    rows, cols = zip(*pixels)
    colors = common.random_colors(4, exclude=[common.green(), common.cyan()])
    flip_horiz, flip_vert = common.randint(0, 1), common.randint(0, 1)

  grid, output = common.grid(size + 3, size + 3), common.grid(size, size)
  for i in range(3 + size):
    grid[i][2] = grid[2][i] = common.cyan()
  grid[0][0] = colors[0]
  grid[0][1] = colors[1]
  grid[1][0] = colors[2]
  grid[1][1] = colors[3]
  for r, c in zip(rows, cols):
    grid[r + 3][c + 3] = common.green()
    if r < size // 2 and c < size // 2:
      color = colors[0]
    elif r < size // 2 and c >= size // 2:
      color = colors[1]
    elif r >= size // 2 and c < size // 2:
      color = colors[2]
    else:
      color = colors[3]
    output[r][c] = color
  if flip_horiz:
    grid, output = common.flip_horiz(grid), common.flip_horiz(output)
  if flip_vert:
    grid, output = grid[::-1], output[::-1]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[0, 0, 1, 1, 1, 1, 1, 1, 2, 2, 3, 3, 4, 4, 4, 4, 4, 4, 5,
                     5],
               cols=[1, 4, 0, 1, 2, 3, 4, 5, 1, 4, 1, 4, 0, 1, 2, 3, 4, 5, 1,
                     4],
               colors=[2, 4, 1, 6], flip_horiz=0, flip_vert=0),
      generate(rows=[0, 0, 0, 1, 1, 2, 2, 2, 2, 3, 4, 4, 4, 4, 4, 4, 5],
               cols=[0, 2, 3, 4, 5, 0, 2, 4, 5, 1, 0, 1, 2, 3, 4, 5, 1],
               colors=[2, 1, 1, 4], flip_horiz=1, flip_vert=0),
      generate(rows=[0, 0, 1, 1, 2, 3, 3, 3, 3, 4, 4, 5, 5],
               cols=[1, 5, 1, 3, 4, 0, 1, 3, 4, 2, 5, 2, 5],
               colors=[6, 5, 2, 4], flip_horiz=0, flip_vert=1),
  ]
  test = [
      generate(rows=[0, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 4, 5],
               cols=[3, 0, 4, 2, 3, 4, 0, 2, 4, 0, 2, 4, 5, 2],
               colors=[7, 4, 1, 2], flip_horiz=1, flip_vert=1),
  ]
  return {"train": train, "test": test}
