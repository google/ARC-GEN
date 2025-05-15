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


def generate(rows=None, cols=None, corners=None, size=7):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    corners: a list of digits specifying which corners are missing
    size: the width and height of the (square) grid
  """
  if rows is None:
    bitmap = common.grid(size, size)
    rows, cols, corners = [], [], []
    for _ in range(common.randint(1, 9)):
      row, col = common.randint(0, size - 2), common.randint(0, size - 2)
      corner = common.randint(0, 3)
      if corner != 0 and common.has_neighbor(size, bitmap, row, col):
        continue
      if corner != 1 and common.has_neighbor(size, bitmap, row, col + 1):
        continue
      if corner != 2 and common.has_neighbor(size, bitmap, row + 1, col):
        continue
      if corner != 3 and common.has_neighbor(size, bitmap, row + 1, col + 1):
        continue
      rows.append(row)
      cols.append(col)
      corners.append(corner)
      bitmap[row][col] = 0 if corner == 0 else 1
      bitmap[row][col + 1] = 0 if corner == 1 else 1
      bitmap[row + 1][col] = 0 if corner == 2 else 1
      bitmap[row + 1][col + 1] = 0 if corner == 3 else 1

  grid, output = common.grids(size, size)
  for r, c, corner in zip(rows, cols, corners):
    grid[r][c] = 0 if corner == 0 else common.cyan()
    grid[r][c + 1] = 0 if corner == 1 else common.cyan()
    grid[r + 1][c] = 0 if corner == 2 else common.cyan()
    grid[r + 1][c + 1] = 0 if corner == 3 else common.cyan()
    output[r][c] = common.blue() if corner == 0 else common.cyan()
    output[r][c + 1] = common.blue() if corner == 1 else common.cyan()
    output[r + 1][c] = common.blue() if corner == 2 else common.cyan()
    output[r + 1][c + 1] = common.blue() if corner == 3 else common.cyan()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[1, 3], cols=[1, 4], corners=[1, 2]),
      generate(rows=[0, 2, 5], cols=[4, 2, 3], corners=[2, 1, 0]),
  ]
  test = [
      generate(rows=[0, 1, 3, 5], cols=[5, 0, 3, 0], corners=[2, 3, 1, 0]),
  ]
  return {"train": train, "test": test}
