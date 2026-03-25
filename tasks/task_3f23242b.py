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


def generate(width=None, height=None, rows=None, cols=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the input grid.
    height: The height of the input grid.
    rows: The rows of the pixels.
    cols: The cols of the pixels.
  """

  if width is None:
    width, height = common.randint(10, 20), common.randint(10, 20)
    row, rows = common.randint(3, 5), []
    while row + 3 < height:
      rows.append(row)
      row += common.randint(5, 6)
    cols = [common.randint(3, width - 4) for _ in range(len(rows))]

  grid, output = common.grids(width, height)
  for row, col in zip(rows, cols):
    output[row][col] = grid[row][col] = 3
    output[row - 1][col] = 5
    for c in range(0, width):
      output[row + 2][c] = 2
    for r in range(row - 1, row + 2):
      output[r][col - 2] = output[r][col + 2] = 2
    for c in range(col - 2, col + 3):
      output[row - 2][c] = 5
      output[row + 2][c] = 8
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=10, height=10, rows=[4], cols=[4]),
      generate(width=16, height=16, rows=[4, 10], cols=[11, 3]),
  ]
  test = [
      generate(width=19, height=17, rows=[3, 8, 13], cols=[4, 11, 6]),
  ]
  return {"train": train, "test": test}
