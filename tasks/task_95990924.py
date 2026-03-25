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


def generate(size=None, rows=None, cols=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: the width and height of the (square) grid
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
  """
  if rows is None:
    factor = common.randint(2, 3)
    size = 5 * factor
    rows, cols, lengths = [], [], []
    for _ in range(3 * factor):
      row, col = common.randint(1, size - 4), common.randint(1, size - 4)
      if common.overlaps(rows + [row], cols + [col], lengths + [4],
                         lengths + [4]): continue
      rows.append(row)
      cols.append(col)
      lengths.append(4)

  grid, output = common.grids(size, size)
  for r, c in zip(rows, cols):
    for dr, dc in [(0, 0), (0, 1), (1, 0), (1, 1)]:
      output[r + dr][c + dc] = grid[r + dr][c + dc] = common.gray()
      output[r + 3 * dr - 1][c + 3 * dc - 1] = 2 * dr + dc + 1
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=10, rows=[3], cols=[4]),
      generate(size=10, rows=[2, 6], cols=[2, 6]),
      generate(size=15, rows=[2, 4, 8, 11], cols=[3, 8, 4, 9]),
  ]
  test = [
      generate(size=15, rows=[1, 1, 4, 6, 10, 11], cols=[1, 11, 5, 12, 2, 9]),
  ]
  return {"train": train, "test": test}
