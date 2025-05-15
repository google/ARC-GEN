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


def generate(rows=None, cols=None, size=9):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    size: the width and height of the (square) grid
  """
  if rows is None:
    rows, cols, lengths = [], [], []
    for _ in range(9):
      r, c = common.randint(1, size - 2), common.randint(1, size - 2)
      if common.overlaps(rows + [r], cols + [c], lengths + [3], lengths + [3]):
        continue
      rows.append(r)
      cols.append(c)
      lengths.append(3)

  grid, output = common.grids(size, size)
  for r, c in zip(rows, cols):
    for dr in [-1, 0, 1]:
      for dc in [-1, 0, 1]:
        output[r + dr][c + dc] = common.blue()
    output[r][c] = grid[r][c] = common.gray()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[1, 4, 7], cols=[6, 3, 1]),
      generate(rows=[1, 2, 5, 7], cols=[7, 3, 7, 3]),
  ]
  test = [
      generate(rows=[1, 2, 4, 7, 7], cols=[1, 7, 3, 1, 5]),
  ]
  return {"train": train, "test": test}
