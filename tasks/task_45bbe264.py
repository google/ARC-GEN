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
    size = common.randint(12, 15)
    pixels = common.randint(2, 3)
    colors = common.random_colors(pixels, exclude=[2])
    while True:
      good = True
      rows = common.sample(range(1, size - 1), pixels)
      cols = common.sample(range(1, size - 1), pixels)
      sorted_rows, sorted_cols = sorted(rows), sorted(cols)
      for i in range(1, pixels):
        if sorted_rows[i - 1] + 1 == sorted_rows[i]: good = False
        if sorted_cols[i - 1] + 1 == sorted_cols[i]: good = False
      if good: break

  grid, output = common.grids(size, size)
  for row, col, color in zip(rows, cols, colors):
    output[row][col] = grid[row][col] = color
    for r in range(size):
      if r != row: output[r][col] = color if output[r][col] == 0 else 2
    for c in range(size):
      if c != col: output[row][c] = color if output[row][c] == 0 else 2
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=14, rows=[5, 10], cols=[9, 3], colors=[3, 4]),
      generate(size=16, rows=[2, 9], cols=[4, 10], colors=[8, 5]),
      generate(size=13, rows=[2, 4, 11], cols=[11, 2, 7], colors=[3, 5, 7]),
  ]
  test = [
      generate(size=15, rows=[2, 6, 12], cols=[3, 10, 6], colors=[8, 4, 1]),
  ]
  return {"train": train, "test": test}
