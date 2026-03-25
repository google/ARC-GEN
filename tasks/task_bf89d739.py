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


def generate(width=None, height=None, trunk=None, rows=None, cols=None, xpose=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: The size of the grid.
    rows: The rows of the boxes.
    cols: The columns of the boxes.
    thicks: The thicknesses of the boxes.
  """

  if width is None:
    width, height = common.randint(10, 20), common.randint(12, 24)
    xpose = common.randint(0, 1)
    while True:
      trunk = common.randint(height // 4, 3 * height // 4)
      length = common.randint(width // 2, width - 2)
      bcol = common.randint(0, width - length)
      rows, cols = [trunk, trunk], [bcol, bcol + length - 1]
      for col in range(cols[0] + 2, cols[1] - 1):
        if common.randint(0, 1): continue
        cdir = common.randint(0, 1)
        if col == cols[-1] + 1: cdir = 1 if rows[-1] < trunk else 0
        cols.append(col)
        rows.append(common.randint(trunk + 2, height - 1) if cdir else common.randint(0, trunk - 2))
      if len(set(rows)) + 1 != len(rows): continue  # Must be distinct!
      if len(rows) >= 4: break

  grid, output = common.grids(width, height)
  for row, col in zip(rows, cols):
    output[row][col] = grid[row][col] = 2
    for r in range(min(row, trunk) + 1, max(row, trunk)):
      output[r][col] = 3
  pair = [c for r, c in zip(rows, cols) if r == trunk]
  for c in range(min(pair) + 1, max(pair)):
    output[trunk][c] = 3
  if xpose: grid, output = common.transpose(grid), common.transpose(output)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=10, height=14, trunk=9, rows=[7, 9, 9, 11], cols=[4, 2, 7, 5], xpose=False),
      generate(width=16, height=12, trunk=5, rows=[2, 5, 5, 8, 10], cols=[6, 2, 12, 10, 7], xpose=True),
      generate(width=14, height=15, trunk=4, rows=[0, 1, 2, 4, 4, 6, 8], cols=[5, 8, 10, 1, 12, 3, 6], xpose=True),
      generate(width=13, height=19, trunk=6, rows=[3, 6, 6, 9, 11], cols=[8, 4, 12, 10, 7], xpose=False),
  ]
  test = [
      generate(width=17, height=14, trunk=8, rows=[3, 6, 8, 8, 10, 12], cols=[6, 4, 1, 12, 10, 8], xpose=False),
  ]
  return {"train": train, "test": test}
