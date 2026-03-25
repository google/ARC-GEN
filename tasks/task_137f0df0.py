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


def generate(rows=None, cols=None):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: The rows of the boxes.
    cols: The columns of the boxes.
  """

  if rows is None:
    row, col, rows, cols = common.randint(0, 2), common.randint(0, 2), [], []
    while row <= 8:
      rows.append(row)
      row += common.randint(3, 4)
    while col <= 8:
      cols.append(col)
      col += common.randint(3, 4)

  grid, output = common.grids(10, 10)
  for row in rows:
    for col in cols:
      for r in range(2):
        for c in range(2):
          output[row + r][col + c] = grid[row + r][col + c] = 5
  for i in range(1, len(rows)):
    for row in range(rows[i - 1] + 2, rows[i]):
      for col in range(10):
        output[row][col] = 1
  for i in range(1, len(cols)):
    for col in range(cols[i - 1] + 2, cols[i]):
      for row in range(10):
        output[row][col] = 1
  for row in range(rows[0], rows[-1] + 2):
    for col in range(cols[0], cols[-1] + 2):
      output[row][col] = 5 if output[row][col] == 5 else 2
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[0, 3, 6], cols=[2, 6]),
      generate(rows=[0, 3, 6], cols=[0, 3, 6]),
      generate(rows=[0, 4, 8], cols=[1, 4, 7]),
  ]
  test = [
      generate(rows=[1, 4, 7], cols=[1, 5, 8]),
  ]
  return {"train": train, "test": test}
