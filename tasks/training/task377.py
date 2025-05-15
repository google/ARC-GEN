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


def generate(width=None, height=None, wides=None, talls=None, rows=None,
             cols=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the input grid
    height: the height of the input grid
    wides: a list of rectangle widths
    talls: a list of rectangle heights
    rows: a list of vertical coordinates where boxes should be placed
    cols: a list of horizontal coordinates where boxes should be placed
    colors: a list of digits representing the box colors to be used
  """
  if width is None:
    width, height = common.randint(20, 30), common.randint(20, 30)
    wides, talls, rows, cols = [width], [height], [0], [0]
    colors = [common.random_color()]
    while True:
      if wides[-1] < 5 or talls[-1] < 5: break
      wide = common.randint(3, wides[-1] - 2)
      tall = common.randint(3, talls[-1] - 2)
      row = common.randint(1, talls[-1] - tall - 1)
      col = common.randint(1, wides[-1] - wide - 1)
      color = common.random_color(exclude=[colors[-1]])
      wides.append(wide)
      talls.append(tall)
      rows.append(row)
      cols.append(col)
      colors.append(color)
      if common.randint(0, 2) == 0: break

  grid = common.grid(width, height, 0)
  output = common.grid(2 * len(colors) - 1, 2 * len(colors) - 1, 0)
  r_off, c_off = 0, 0
  for w, h, r, c, color in zip(wides, talls, rows, cols, colors):
    for row in range(r, r + h):
      for col in range(c, c + w):
        grid[r_off + row][c_off + col] = color
    r_off, c_off = r_off + r, c_off + c
  for idx, color in enumerate(colors):
    for r in range(idx, 2 * len(colors) - idx - 1):
      for c in range(idx, 2 * len(colors) - idx - 1):
        output[r][c] = color
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=27, height=23, wides=[27, 18, 6], talls=[23, 16, 6],
               rows=[0, 2, 7], cols=[0, 3, 3], colors=[8, 3, 2]),
      generate(width=25, height=22, wides=[25, 15], talls=[22, 13], rows=[0, 3],
               cols=[0, 4], colors=[5, 6]),
      generate(width=22, height=21, wides=[22, 14, 9, 5], talls=[21, 14, 9, 3],
               rows=[0, 3, 2, 1], cols=[0, 3, 2, 3], colors=[3, 8, 2, 1]),
  ]
  test = [
      generate(width=27, height=26, wides=[27, 20, 14, 9, 4],
               talls=[26, 19, 14, 7, 4], rows=[0, 5, 2, 3, 1],
               cols=[0, 3, 3, 3, 3], colors=[2, 1, 3, 8, 2]),
  ]
  return {"train": train, "test": test}
