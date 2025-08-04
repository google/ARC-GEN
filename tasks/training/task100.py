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


def generate(rows=None, cols=None, wides=None, talls=None, colors=None,
             xpose=None, size=10):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where boxes should be placed
    cols: a list of horizontal coordinates where boxes should be placed
    wides: a list of widths of the boxes
    talls: a list of heights of the boxes
    colors: a list of colors of the boxes
    xpose: whether to transpose the grid
    size: the width and height of the (square) grid
  """
  if rows is None:
    while True:
      tall0 = common.randint(3, 7)
      tall1 = common.randint(3, size - tall0)
      wide0, wide1 = common.randint(3, size), common.randint(3, size)
      if wide0 * tall0 != wide1 * tall1: break
    wides, talls = [wide0, wide1], [tall0, tall1]
    rows = [0, tall0 + (0 if tall0 + tall1 == size else 1)]  # maybe add space
    cols = [common.randint(0, size - wide0), common.randint(0, size - wide1)]
    colors, xpose = common.random_colors(2), common.randint(0, 1)

  grid, output = common.grid(size, size), common.grid(2, 2)
  for row, col, wide, tall, color in zip(rows, cols, wides, talls, colors):
    for r in range(row, row + tall):
      grid[r][col + wide - 1] = grid[r][col] = color
    for c in range(col, col + wide):
      grid[row][c] = grid[row + tall - 1][c] = color
  for r, c in [(0, 0), (0, 1), (1, 0), (1, 1)]:
    output[r][c] = colors[0 if wides[0] * talls[0] > wides[1] * talls[1] else 1]
  if xpose: grid = common.transpose(grid)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[0, 5], cols=[1, 3], wides=[4, 5], talls=[4, 4],
               colors=[7, 8], xpose=0),
      generate(rows=[0, 5], cols=[0, 2], wides=[5, 6], talls=[4, 4],
               colors=[6, 7], xpose=0),
      generate(rows=[0, 7], cols=[1, 7], wides=[6, 3], talls=[7, 3],
               colors=[4, 2], xpose=0),
  ]
  test = [
      generate(rows=[0, 6], cols=[0, 0], wides=[9, 10], talls=[5, 4],
               colors=[3, 9], xpose=1),
  ]
  return {"train": train, "test": test}
