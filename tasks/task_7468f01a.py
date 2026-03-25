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


def generate(width=None, height=None, rows=None, cols=None, colors=None,
             wide=None, tall=None, rowoffset=None, coloffset=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the input grid
    height: the height of the input grid
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    colors: a pair of digits to be used for colors
    wide: the width of the output grid
    tall: the height of the output grid
    rowoffset: the vertical offset of the output grid
    coloffset: the horizontal offset of the output grid
  """
  if width is None:
    width, height = common.randint(10, 20), common.randint(10, 20)
    wide, tall = common.randint(4, 8), common.randint(4, 8)
    rowoffset = common.randint(1, height - tall - 1)
    coloffset = common.randint(1, width - wide - 1)
    bitmap = common.grid(wide, tall, 0)
    for _ in range(common.randint(1, 3)):
      pixels = common.continuous_creature(common.randint(1, 5))
      row, col = common.randint(0, tall - 3), common.randint(0, wide - 3)
      for p in pixels:
        bitmap[row + p[0]][col + p[1]] = 1
    rows, cols = [], []
    for r in range(tall):
      for c in range(wide):
        if not bitmap[r][c]: continue
        rows.append(r)
        cols.append(c)
    colors = common.random_colors(2)

  grid, output = common.grid(width, height), common.grid(wide, tall)
  for r in range(tall):
    for c in range(wide):
      output[r][c] = grid[r + rowoffset][c + coloffset] = colors[0]
  for row, col in zip(rows, cols):
    grid[row + rowoffset][col + coloffset] = colors[1]
    output[row][wide - col - 1] = colors[1]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=15, height=10, rows=[0, 1, 1, 2, 2], cols=[6, 1, 2, 2, 3],
               colors=[8, 2], wide=8, tall=4, rowoffset=5, coloffset=2),
      generate(width=16, height=12, rows=[2, 2, 3, 3, 4], cols=[1, 2, 2, 3, 2],
               colors=[4, 1], wide=5, tall=5, rowoffset=1, coloffset=3),
      generate(width=17, height=15, rows=[0, 1, 1, 1, 2, 3],
               cols=[3, 1, 2, 3, 4, 4], colors=[6, 3], wide=6, tall=4,
               rowoffset=7, coloffset=2),
  ]
  test = [
      generate(width=17, height=17, rows=[0, 1, 1, 3, 3, 3, 5, 5, 5],
               cols=[4, 5, 6, 0, 1, 2, 2, 3, 4], colors=[1, 8], wide=8, tall=7,
               rowoffset=3, coloffset=3),
  ]
  return {"train": train, "test": test}
