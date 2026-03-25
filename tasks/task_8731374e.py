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


def generate(width=None, height=None, wide=None, tall=None, rowoffset=None,
             coloffset=None, rows=None, cols=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the (square) grid
    height: the height of the (square) grid
    wide: the width of the box
    tall: the height of the box
    rowoffset: the vertical offset of the box
    coloffset: the horizontal offset of the box
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    colors: a list of colors for the pixels
  """
  if width is None:
    width, height = common.randint(15, 30), common.randint(15, 30)
    wide, tall = common.randint(6, 10), common.randint(6, 10)
    rowoffset = common.randint(1, height - tall - 1)
    coloffset = common.randint(1, width - wide - 1)
    colors = [common.randint(0, 9) for _ in range(width * height)]
    color_list = common.sample(range(10), 2)
    color, boxcolor = color_list[0], color_list[1]
    for r in range(tall):
      for c in range(wide):
        colors[(rowoffset + r) * width + coloffset + c] = boxcolor
    num_pixels = common.randint(1, 3)
    rows = common.sample(range(1, tall - 1), num_pixels)
    cols = common.sample(range(1, wide - 1), num_pixels)
    for r, c in zip(rows, cols):
      colors[(rowoffset + r) * width + coloffset + c] = color

  grid, output = common.grid(width, height), common.grid(wide, tall)
  for r in range(height):
    for c in range(width):
      grid[r][c] = colors[r * width + c]
  for r in range(tall):
    for c in range(wide):
      output[r][c] = grid[rowoffset + r][coloffset + c]
  for row, col in zip(rows, cols):
    for r in range(tall):
      output[r][col] = grid[rowoffset + row][coloffset + col]
    for c in range(wide):
      output[row][c] = grid[rowoffset + row][coloffset + col]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=23, height=17, wide=6, tall=7, rowoffset=5, coloffset=8,
               rows=[2, 4], cols=[4, 1],
               colors=[6, 1, 2, 4, 8, 3, 7, 2, 6, 5, 7, 7, 4, 9, 2, 5, 9, 4, 5,
                       9, 3, 8, 7, 6, 0, 1, 0, 4, 8, 6, 1, 1, 2, 1, 2, 6, 6, 6,
                       5, 8, 7, 4, 1, 7, 5, 6, 6, 8, 3, 1, 9, 8, 7, 1, 2, 3, 9,
                       2, 6, 2, 1, 0, 5, 7, 7, 7, 8, 1, 3, 2, 2, 9, 5, 5, 6, 6,
                       9, 3, 8, 6, 2, 4, 1, 8, 3, 5, 7, 5, 5, 6, 1, 6, 1, 7, 6,
                       4, 7, 0, 1, 7, 9, 1, 7, 6, 9, 6, 6, 8, 4, 6, 8, 8, 9, 8,
                       0, 2, 9, 2, 3, 9, 6, 8, 8, 1, 1, 1, 1, 1, 1, 9, 7, 2, 4,
                       0, 1, 6, 4, 5, 8, 3, 9, 5, 6, 5, 6, 8, 1, 1, 1, 1, 1, 1,
                       3, 0, 1, 3, 1, 6, 3, 5, 1, 0, 7, 2, 6, 5, 2, 0, 7, 1, 1,
                       1, 1, 2, 1, 2, 2, 3, 0, 7, 5, 1, 8, 8, 2, 4, 7, 2, 7, 0,
                       9, 3, 1, 1, 1, 1, 1, 1, 4, 7, 7, 6, 2, 0, 0, 0, 4, 5, 1,
                       3, 2, 7, 5, 2, 8, 1, 2, 1, 1, 1, 1, 4, 6, 4, 7, 5, 2, 8,
                       9, 6, 6, 8, 2, 6, 8, 4, 6, 7, 1, 1, 1, 1, 1, 1, 8, 2, 1,
                       7, 9, 1, 2, 9, 1, 1, 1, 9, 9, 4, 7, 2, 2, 1, 1, 1, 1, 1,
                       1, 3, 9, 2, 4, 9, 3, 6, 4, 5, 5, 9, 4, 8, 5, 8, 8, 1, 5,
                       3, 8, 8, 4, 7, 6, 4, 1, 1, 8, 5, 6, 2, 2, 1, 1, 4, 7, 9,
                       1, 5, 6, 8, 2, 3, 2, 2, 4, 4, 8, 6, 5, 6, 8, 5, 8, 3, 9,
                       4, 2, 5, 1, 7, 4, 8, 1, 8, 5, 5, 7, 9, 1, 8, 5, 3, 1, 8,
                       0, 2, 0, 2, 9, 2, 7, 1, 5, 2, 2, 8, 6, 9, 3, 9, 6, 6, 3,
                       6, 2, 2, 6, 1, 4, 6, 6, 5, 3, 7, 0, 9, 1, 3, 2, 6, 5, 0,
                       6, 1, 0, 5, 2, 7, 1, 4, 8, 4, 1]),
      generate(width=23, height=27, wide=9, tall=10, rowoffset=6, coloffset=4,
               rows=[2, 5, 7], cols=[2, 6, 4],
               colors=[3, 1, 8, 2, 5, 1, 9, 5, 0, 5, 1, 2, 4, 2, 9, 7, 4, 4, 5,
                       8, 6, 7, 6, 5, 6, 8, 3, 9, 8, 4, 1, 2, 1, 5, 3, 2, 4, 6,
                       1, 8, 7, 6, 6, 9, 9, 0, 6, 8, 6, 0, 2, 0, 2, 5, 2, 8, 0,
                       2, 1, 9, 5, 8, 1, 2, 9, 4, 7, 4, 4, 8, 5, 7, 4, 4, 4, 1,
                       9, 8, 2, 5, 7, 6, 6, 0, 8, 3, 7, 8, 1, 0, 9, 9, 0, 3, 8,
                       2, 6, 4, 9, 5, 3, 5, 4, 9, 5, 5, 4, 0, 8, 1, 5, 2, 1, 1,
                       0, 8, 4, 7, 9, 5, 2, 3, 0, 8, 0, 1, 7, 6, 4, 2, 0, 8, 7,
                       3, 9, 5, 5, 6, 5, 6, 0, 8, 4, 4, 4, 4, 4, 4, 4, 4, 4, 0,
                       6, 4, 9, 8, 2, 6, 3, 8, 2, 0, 0, 1, 3, 4, 4, 4, 4, 4, 4,
                       4, 4, 4, 6, 7, 7, 0, 4, 4, 0, 4, 1, 4, 7, 3, 3, 1, 4, 4,
                       1, 4, 4, 4, 4, 4, 4, 6, 5, 0, 8, 5, 9, 7, 3, 9, 1, 9, 3,
                       0, 6, 4, 4, 4, 4, 4, 4, 4, 4, 4, 2, 6, 1, 4, 0, 4, 6, 4,
                       7, 0, 5, 0, 8, 1, 4, 4, 4, 4, 4, 4, 4, 4, 4, 7, 4, 8, 3,
                       6, 4, 3, 4, 3, 5, 4, 6, 4, 3, 4, 4, 4, 4, 4, 4, 1, 4, 4,
                       2, 6, 1, 0, 8, 1, 1, 8, 8, 1, 7, 4, 8, 2, 4, 4, 4, 4, 4,
                       4, 4, 4, 4, 0, 0, 2, 1, 5, 7, 9, 2, 5, 0, 2, 5, 2, 4, 4,
                       4, 4, 4, 1, 4, 4, 4, 4, 1, 4, 3, 3, 1, 2, 8, 7, 9, 9, 6,
                       4, 5, 6, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5, 5, 9, 6, 1, 7, 9,
                       9, 7, 8, 3, 8, 6, 1, 4, 4, 4, 4, 4, 4, 4, 4, 4, 2, 3, 4,
                       3, 7, 4, 6, 3, 7, 6, 1, 0, 1, 4, 5, 0, 7, 9, 1, 9, 6, 5,
                       6, 1, 6, 4, 5, 1, 3, 0, 2, 3, 9, 4, 6, 4, 6, 2, 7, 0, 8,
                       5, 9, 4, 1, 7, 0, 9, 1, 3, 7, 7, 5, 4, 1, 7, 2, 0, 6, 6,
                       0, 3, 8, 6, 7, 3, 3, 8, 2, 6, 8, 5, 7, 1, 1, 8, 4, 3, 9,
                       9, 4, 3, 8, 6, 2, 9, 0, 7, 1, 3, 5, 7, 8, 7, 6, 1, 0, 2,
                       2, 2, 5, 3, 3, 8, 2, 2, 3, 6, 2, 4, 0, 2, 3, 9, 9, 1, 6,
                       3, 4, 6, 7, 9, 7, 0, 8, 1, 9, 4, 5, 8, 3, 8, 3, 7, 6, 6,
                       6, 9, 2, 3, 4, 7, 9, 6, 1, 3, 3, 3, 2, 3, 9, 3, 9, 6, 6,
                       3, 2, 8, 0, 3, 6, 4, 5, 0, 9, 9, 8, 1, 4, 4, 0, 7, 6, 6,
                       4, 1, 9, 6, 8, 5, 3, 2, 5, 6, 8, 9, 6, 4, 2, 6, 3, 4, 7,
                       9, 4, 1, 7, 6, 6, 7, 4, 3, 0, 2, 0, 7, 1, 7, 3, 0, 2, 0,
                       3, 8, 6, 2, 7, 2, 5, 4, 4, 0, 8, 2, 8, 9, 8, 9, 7, 8, 5,
                       3, 3, 2, 5, 7, 4, 0, 3, 7, 2, 5, 5, 0, 0, 4, 2, 4, 9, 9,
                       3, 1, 6, 1, 1, 6, 5, 9, 8, 3, 7, 4, 2]),
      generate(width=17, height=16, wide=8, tall=6, rowoffset=2, coloffset=5,
               rows=[3], cols=[3],
               colors=[0, 0, 7, 9, 8, 8, 0, 8, 9, 9, 3, 1, 4, 5, 2, 7, 6, 6, 0,
                       9, 2, 7, 2, 8, 4, 3, 3, 2, 7, 7, 5, 9, 4, 0, 1, 9, 4, 5,
                       4, 8, 8, 8, 8, 8, 8, 8, 8, 2, 0, 7, 9, 5, 5, 6, 8, 3, 8,
                       8, 8, 8, 8, 8, 8, 8, 2, 0, 2, 7, 8, 2, 3, 2, 9, 8, 8, 8,
                       8, 8, 8, 8, 8, 0, 7, 6, 4, 1, 7, 3, 3, 5, 8, 8, 8, 2, 8,
                       8, 8, 8, 7, 1, 1, 4, 7, 2, 3, 5, 6, 8, 8, 8, 8, 8, 8, 8,
                       8, 5, 8, 5, 6, 5, 2, 7, 3, 5, 8, 8, 8, 8, 8, 8, 8, 8, 1,
                       4, 4, 6, 1, 4, 0, 0, 9, 9, 4, 0, 2, 6, 5, 5, 0, 8, 6, 4,
                       7, 8, 7, 8, 3, 3, 8, 0, 9, 0, 4, 8, 9, 8, 5, 2, 7, 3, 2,
                       0, 2, 8, 2, 0, 8, 4, 4, 3, 2, 6, 8, 7, 4, 7, 2, 2, 7, 8,
                       3, 7, 4, 2, 4, 8, 4, 2, 3, 9, 9, 2, 0, 8, 4, 8, 8, 5, 3,
                       2, 0, 1, 8, 9, 3, 9, 8, 1, 8, 8, 7, 3, 9, 9, 9, 1, 6, 1,
                       9, 4, 7, 5, 5, 3, 2, 9, 3, 0, 5, 8, 2, 5, 4, 2, 2, 4, 0,
                       9, 2, 8, 1, 3, 5, 7, 3, 8, 0, 9, 5, 3, 8, 4, 5, 0, 2, 5,
                       2, 9, 6, 0, 1, 0]),
  ]
  test = [
      generate(width=17, height=19, wide=8, tall=10, rowoffset=2, coloffset=3,
               rows=[2, 5], cols=[6, 2],
               colors=[2, 7, 2, 0, 2, 6, 3, 0, 3, 9, 1, 3, 5, 3, 0, 4, 5, 4, 4,
                       8, 7, 0, 7, 9, 1, 4, 9, 5, 2, 0, 8, 5, 3, 2, 8, 7, 9, 8,
                       8, 8, 8, 8, 8, 8, 8, 7, 6, 1, 5, 2, 1, 6, 9, 3, 8, 8, 8,
                       8, 8, 8, 8, 8, 7, 7, 8, 1, 3, 6, 0, 2, 9, 8, 8, 8, 8, 8,
                       8, 1, 8, 9, 5, 1, 9, 4, 1, 5, 2, 6, 8, 8, 8, 8, 8, 8, 8,
                       8, 8, 3, 6, 7, 9, 5, 8, 4, 4, 8, 8, 8, 8, 8, 8, 8, 8, 8,
                       7, 1, 7, 3, 7, 8, 6, 2, 8, 8, 1, 8, 8, 8, 8, 8, 6, 3, 1,
                       1, 2, 9, 9, 4, 0, 8, 8, 8, 8, 8, 8, 8, 8, 6, 4, 0, 6, 7,
                       6, 6, 7, 7, 8, 8, 8, 8, 8, 8, 8, 8, 4, 7, 1, 5, 8, 4, 4,
                       0, 3, 8, 8, 8, 8, 8, 8, 8, 8, 4, 2, 4, 3, 4, 5, 3, 7, 7,
                       8, 8, 8, 8, 8, 8, 8, 8, 4, 8, 7, 7, 1, 8, 6, 6, 4, 7, 6,
                       8, 1, 8, 1, 9, 2, 6, 8, 7, 2, 8, 8, 7, 3, 5, 1, 4, 1, 6,
                       4, 9, 6, 7, 7, 9, 2, 3, 0, 2, 9, 2, 2, 5, 4, 8, 3, 9, 9,
                       9, 5, 9, 6, 1, 4, 6, 9, 6, 1, 9, 6, 3, 1, 6, 6, 8, 6, 0,
                       1, 3, 4, 8, 7, 7, 2, 1, 2, 4, 9, 2, 1, 5, 1, 7, 0, 7, 9,
                       3, 8, 2, 1, 7, 1, 9, 4, 2, 8, 4, 3, 6, 2, 8, 0, 8, 5, 3,
                       5, 9, 1, 2, 5, 7, 8, 7, 1, 6, 5, 8, 0, 9, 2, 8, 9, 1,
                       5]),
  ]
  return {"train": train, "test": test}
