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


def generate(rows=None, cols=None, size=15):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    size: the width and height of the (square) grid
  """
  if rows is None:
    rows, cols = [], []
    for _ in range(2):
      row, col = common.randint(3, 11), common.randint(3, 11)
      overlaps = False
      for r, c in zip(rows, cols):
        # Boxes can't overlap, and also their crosshairs shouldn't touch.
        overlaps = overlaps or (abs(r - row) < 6 and abs(c - col) < 6)
        overlaps = overlaps or abs(r - row) < 3 or abs(c - col) < 3
      if overlaps: continue
      rows.append(row)
      cols.append(col)

  grid, output = common.grids(size, size, common.cyan())
  for r, c in zip(rows, cols):
    for i in range(size):
      output[r][i] = output[i][c] = common.pink()
  for r, c in zip(rows, cols):
    for i in range(5):
      output[r - 2][c - 2 + i] = grid[r - 2][c - 2 + i] = common.blue()
      output[r + 2][c - 2 + i] = grid[r + 2][c - 2 + i] = common.blue()
      output[r - 2 + i][c - 2] = grid[r - 2 + i][c - 2] = common.blue()
      output[r - 2 + i][c + 2] = grid[r - 2 + i][c + 2] = common.blue()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[3], cols=[5]),
      generate(rows=[5, 11], cols=[5, 10]),
  ]
  test = [
      generate(rows=[3, 11], cols=[8, 5]),
  ]
  return {"train": train, "test": test}
