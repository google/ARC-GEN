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


def generate(size=None, rows=None, cols=None, lengths=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: the width and height of the (square) grid
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    lengths: a list of lengths of the boxes
  """
  if size is None:
    size = common.randint(10, 20)
    num_boxes = common.randint(size // 4, size // 3)
    while True:
      lengths = [common.randint(3, 10) for _ in range(num_boxes)]
      rows = [common.randint(0, size - length) for length in lengths]
      cols = [common.randint(0, size - length) for length in lengths]
      if not common.overlaps(rows, cols, lengths, lengths, 1): break

  grid, output = common.grids(size, size)
  for row, col, length in zip(rows, cols, lengths):
    for r in range(row, row + length):
      grid[r][col] = grid[r][col + length - 1] = common.blue()
      output[r][col] = output[r][col + length - 1] = common.blue()
    for c in range(col, col + length):
      grid[row][c] = grid[row + length - 1][c] = common.blue()
      output[row][c] = output[row + length - 1][c] = common.blue()
    for r in range(row + 1, row + length - 1):
      for c in range(col + 1, col + length - 1):
        output[r][c] = common.orange() if length % 2 else common.red()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=10, rows=[0, 2, 5], cols=[0, 6, 0], lengths=[4, 3, 5]),
      generate(size=10, rows=[0, 0], cols=[0, 4], lengths=[3, 6]),
      generate(size=20, rows=[0, 1, 3, 9, 12], cols=[0, 6, 12, 2, 12],
               lengths=[5, 4, 6, 7, 8]),
      generate(size=11, rows=[1, 2, 6], cols=[1, 5, 0], lengths=[3, 4, 5]),
      generate(size=15, rows=[1, 9], cols=[1, 6], lengths=[7, 6]),
  ]
  test = [
      generate(size=20, rows=[0, 2, 7, 11], cols=[12, 1, 10, 1],
               lengths=[5, 8, 10, 7]),
  ]
  return {"train": train, "test": test}
