# Copyright 2026 Google LLC
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


def generate(width=None, rows=None, cols=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the grid.
    rows: The rows of the boxes.
    cols: The columns of the boxes.
  """

  if width is None:
    width = common.randint(5, 17)
    while True:
      col, cols = common.randint(0, 1), []
      row, rows = common.randint(0, 5), []
      last_spacing = 2
      while col + 1 < width:
        cols.append(col)
        rows.append(row)
        spacing = common.randint(1 if last_spacing > 1 else 2, 3)
        last_spacing = spacing
        col += spacing
        while True:
          row = common.randint(0, 5)
          if row == rows[-1]: continue
          if spacing == 2 and row in [rows[-1] - 1, rows[-1], rows[-1] + 1]: continue
          if spacing == 1 and row in [rows[-1] - 2, rows[-1] - 1, rows[-1], rows[-1] + 1, rows[-1] + 2]: continue
          break
      if cols[-1] + 2 == width: break  # I guess they all end @ the right wall.

  grid, output = common.grids(width, 7)
  for i in range(len(rows)):
    row, col = rows[i], cols[i]
    for dr in [0, 1]:
      for dc in [0, 1]:
        grid[row + dr][col + dc] = 2
        output[row + dr][col + dc] = 2 if i % 2 == len(rows) % 2 else 8
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=7, rows=[2, 4, 1], cols=[0, 2, 5]),
      generate(width=14, rows=[1, 4, 1, 4, 2, 0], cols=[1, 3, 4, 7, 9, 12]),
      generate(width=15, rows=[5, 2, 4, 0, 3, 5, 1], cols=[0, 2, 5, 6, 8, 11, 13]),
      generate(width=5, rows=[1, 4], cols=[0, 3]),
      generate(width=17, rows=[0, 3, 1, 5, 2, 4, 0, 3, 5], cols=[0, 1, 4, 6, 7, 10, 11, 13, 15]),
  ]
  test = [
      generate(width=15, rows=[5, 2, 4, 1, 5, 4, 1], cols=[0, 2, 4, 7, 8, 11, 13]),
  ]
  return {"train": train, "test": test}
