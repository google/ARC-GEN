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


def generate(width=None, height=None, rows=None, cols=None, flip=None,
             flop=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the grid.
    height: The height of the grid.
    rows: The rows of the pixels.
    cols: The columns of the pixels.
    flip: Whether to flip the grid.
    flop: Whether to flop the grid.
  """

  if width is None:
    width, height = common.randint(12, 16), common.randint(12, 16)
    while True:
      rows = sorted([common.randint(0, height - 1) for _ in range(2)], reverse=True)
      cols = sorted([common.randint(0, width - 1) for _ in range(2)])
      if rows[1] + 3 <= rows[0] and cols[0] + 3 <= cols[1]: break
    flip, flop = common.randint(0, 1), common.randint(0, 1)

  grid, output = common.grids(width, height)
  output[rows[0]][cols[0]] = grid[rows[0]][cols[0]] = 1
  output[rows[1]][cols[1]] = grid[rows[1]][cols[1]] = 2
  row, col = rows[0], cols[0]
  while col + 1 < cols[1] and row - 1 > rows[1]:
    row, col = row - 1, col + 1
    output[row][col] = 3
  while col + 1 < cols[1] or row - 1 > rows[1]:
    if col + 1 < cols[1]: col += 1
    if row - 1 > rows[1]: row -= 1
    output[row][col] = 3
  if flip: grid, output = common.flip(grid), common.flip(output)
  if flop: grid, output = common.flop(grid), common.flop(output)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=16, height=15, rows=[12, 1], cols=[3, 6], flip=False, flop=False),
      generate(width=12, height=15, rows=[13, 1], cols=[3, 10], flip=False, flop=True),
      generate(width=16, height=16, rows=[14, 2], cols=[4, 12], flip=True, flop=True),
      generate(width=12, height=13, rows=[10, 3], cols=[1, 11], flip=False, flop=False),
  ]
  test = [
      generate(width=16, height=16, rows=[14, 2], cols=[4, 12], flip=True, flop=False),
  ]
  return {"train": train, "test": test}
