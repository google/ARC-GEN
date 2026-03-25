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


def generate(size=None, rows=None, cols=None, thicks=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: The size of the grid.
    rows: The rows of the boxes.
    cols: The columns of the boxes.
    thicks: The thicknesses of the boxes.
  """

  colors = [8, 4, 3]
  if size is None:
    size = common.randint(7, 23)
    max_thick = 2 if size < 9 else 3
    num_boxes = size // 4 - 1
    while True:
      thicks = [common.randint(1, max_thick) for _ in range(num_boxes)]
      sizes = [2 * thick + 3 for thick in thicks]
      rows = [common.randint(0, size - s) for s in sizes]
      cols = [common.randint(0, size - s) for s in sizes]
      if not common.overlaps(rows, cols, sizes, sizes, 1): break

  grid, output = common.grids(size, size)
  for row, col, thick in zip(rows, cols, thicks):
    length = 2 * thick + 3
    for r in range(length):
      for c in range(length):
        output[row + r][col + c] = colors[thick - 1]
    grid[row + thick + 1][col + thick + 1] = 2
    output[row + thick + 1][col + thick + 1] = 2
    for i in range(length):
      output[row + i][col] = grid[row + i][col] = 2
      output[row][col + i] = grid[row][col + i] = 2
      output[row + i][col + length - 1] = grid[row + i][col + length - 1] = 2
      output[row + length - 1][col + i] = grid[row + length - 1][col + i] = 2
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=15, rows=[0, 10], cols=[6, 1], thicks=[3, 1]),
      generate(size=9, rows=[0], cols=[0], thicks=[2]),
      generate(size=13, rows=[0, 6], cols=[1, 5], thicks=[1, 2]),
      generate(size=7, rows=[0], cols=[0], thicks=[1]),
  ]
  test = [
      generate(size=20, rows=[0, 1, 7, 12], cols=[11, 1, 13, 5],
               thicks=[1, 3, 1, 2]),
  ]
  return {"train": train, "test": test}
