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


def generate(size=None, rows=None, cols=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: The size of the grid.
    rows: The rows of the pixels.
    cols: The columns of the pixels.
    colors: The colors of the pixels.
  """

  if size is None:
    base = common.randint(2, 3)
    size = 3 * base
    colors = common.shuffle([1, 2, 3, 4, 5, 6, 7, 8, 9])
    rows, cols = [], []
    for i in range(9):
      r, c = base * (i // 3), base * (i % 3)
      rows.append(r + common.randint(0, base - 1))
      cols.append(c + common.randint(0, base - 1))

  grid, output = common.grid(size, size), common.grid(3, 3)
  for row, col, color in zip(rows, cols, colors):
    grid[row][col] = color
  for i, color in enumerate(colors):
    output[i // 3][i % 3] = color
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=9, rows=[1, 0, 0, 5, 3, 4, 6, 7, 6],
               cols=[1, 3, 6, 0, 5, 8, 2, 4, 6],
               colors=[4, 7, 8, 5, 2, 1, 3, 9, 6]),
      generate(size=6, rows=[0, 1, 0, 2, 3, 2, 5, 4, 5],
               cols=[1, 3, 5, 0, 2, 4, 0, 3, 4],
               colors=[6, 4, 7, 2, 3, 9, 1, 5, 8]),
      generate(size=6, rows=[0, 0, 1, 2, 3, 2, 5, 4, 5],
               cols=[0, 3, 5, 1, 2, 4, 0, 3, 4],
               colors=[2, 1, 7, 3, 5, 9, 4, 6, 8]),
  ]
  test = [
      generate(size=9, rows=[1, 1, 0, 5, 4, 3, 7, 7, 8],
               cols=[0, 5, 6, 2, 5, 7, 1, 3, 8],
               colors=[5, 6, 9, 4, 1, 8, 3, 2, 7]),
  ]
  return {"train": train, "test": test}
