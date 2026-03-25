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


def generate(width=None, height=None, rows=None, cols=None, wides=None,
             talls=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the input grid
    height: the height of the input grid
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    wides: a list of box widths
    talls: a list of box heights
    colors: a list of colors to be used for pixels
  """
  if rows is None:
    width, height = common.randint(8, 16), common.randint(8, 16)
    rows, cols, wides, talls = [], [], [], []
    row = 1
    while True:
      wide = common.randint(4, width - 1)
      tall = common.randint(3, wide - 1)
      if row + tall > height: break
      col = common.randint(0, width - wide)
      rows.append(row)
      cols.append(col)
      wides.append(wide)
      talls.append(tall)
      row += tall + 1
    colors = common.random_colors(len(rows))

  grid, output = common.grids(width, height)
  for row, col, wide, tall, color in zip(rows, cols, wides, talls, colors):
    # Horizontal stuff.
    for c in range(wide - tall + 2):
      grid[row][col + c] = color
      grid[row + tall - 1][col + c + tall - 2] = color
      output[row][col + c + 1] = color
      output[row + tall - 1][col + c + tall - 2] = color
    # Diagonal stuff
    for r in range(1, tall - 1):
      grid[row + r][col + r - 1] = color
      grid[row + r][col + r + wide - tall + 1] = color
      output[row + r][col + r] = color
      output[row + r][min(col + r + wide - tall + 2, col + wide - 1)] = color
  return {"input": grid, "output": output}



def validate():
  """Validates the generator."""
  train = [
      generate(width=9, height=14, rows=[1, 7], cols=[1, 2], wides=[6, 4],
               talls=[5, 3], colors=[6, 2]),
      generate(width=9, height=8, rows=[1], cols=[1], wides=[8], talls=[5],
               colors=[8]),
  ]
  test = [
      generate(width=10, height=10, rows=[1], cols=[1], wides=[9], talls=[5],
               colors=[4]),
  ]
  return {"train": train, "test": test}
