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


def generate(width=None, height=None, rows=None, cols=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the input grid
    height: the height of the input grid
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
  """
  if width is None:
    width, height = common.randint(3, 15), common.randint(3, 15)
    bitmap = common.grid(width, height, 0)
    rows, cols = [], []
    # First, create some lines
    for _ in range(3):
      if common.randint(0, 1) == 0:  # horizontal
        row = common.randint(0, height - 1)
        col = common.sample(range(0, width), 2)
        col.sort()
        if col[0] + 1 == col[1]: continue  # Too short
        # Need to check that we don't line up with others, and don't cross paths
        cross = False
        for c in range(col[0], col[1] + 1):
          cross = cross or bitmap[row][c] == 1
        if cross or row in rows or col[0] in cols or col[1] in cols: continue
        rows.extend([row, row])
        cols.extend(col)
        for c in range(col[0], col[1] + 1):
          bitmap[row][c] = 1
      else:
        row = common.sample(range(0, height), 2)
        col = common.randint(0, width - 1)
        row.sort()
        if row[0] + 1 == row[1]: continue  # Too short
        # Need to check that we don't line up with others, and don't cross paths
        cross = False
        for r in range(row[0], row[1] + 1):
          cross = cross or bitmap[r][col] == 1
        if cross or row[0] in rows or row[1] in rows or col in cols: continue
        rows.extend(row)
        cols.extend([col, col])
        for r in range(row[0], row[1] + 1):
          bitmap[r][col] = 1
    # Second, create some unconnected points
    for _ in range(2):
      row, col = common.randint(0, height - 1), common.randint(0, width - 1)
      if bitmap[row][col] == 1 or row in rows or col in cols: continue
      bitmap[row][col] = 1
      rows.append(row)
      cols.append(col)

  grid, output = common.grids(width, height)
  for r, c in zip(rows, cols):
    output[r][c] = grid[r][c] = common.cyan()
  for j in range(len(rows)):
    for i in range(j):
      if rows[i] == rows[j]:
        min_col, max_col = min(cols[i], cols[j]), max(cols[i], cols[j])
        for c in range(min_col + 1, max_col):
          output[rows[i]][c] = common.green()
      if cols[i] == cols[j]:
        min_row, max_row = min(rows[i], rows[j]), max(rows[i], rows[j])
        for r in range(min_row + 1, max_row):
          output[r][cols[i]] = common.green()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=13, height=7, rows=[3, 3], cols=[2, 9]),
      generate(width=11, height=10, rows=[1, 2, 6, 7], cols=[4, 8, 8, 4]),
      generate(width=11, height=12, rows=[1, 1, 8, 8], cols=[1, 9, 2, 7]),
      generate(width=6, height=9, rows=[1, 7], cols=[2, 2]),
      generate(width=3, height=3, rows=[1], cols=[1]),
      generate(width=6, height=5, rows=[1, 3], cols=[1, 4]),
      generate(width=6, height=7, rows=[1, 3, 6], cols=[3, 1, 3]),
      generate(width=11, height=12,
               rows=[1, 4, 4, 5, 9], cols=[3, 6, 10, 1, 3]),
  ]
  test = [
      generate(width=13, height=12, rows=[1, 1, 5, 5, 7, 9, 10],
               cols=[2, 10, 6, 12, 1, 8, 1]),
  ]
  return {"train": train, "test": test}
