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


def generate(size=None, rows=None, cols=None, lengths=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: the width and height of the (square) grid
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    lengths: the lengths of the flower centers
    colors: two digits representing the colors to be used
  """
  if size is None:
    size, colors = common.randint(10, 12), common.random_colors(2)
    rows, cols, lengths = [], [], []
    for _ in range(2):
      length = common.randint(1, 2)
      row = common.randint(length + 1, size - length * 2 - 1)
      col = common.randint(length + 1, size - length * 2 - 1)
      overlaps = False
      for r, c, l in zip(rows, cols, lengths):
        if r + 2 * l < row - length or row + 2 * length < r - l: continue
        if c + 2 * l < col - length or col + 2 * length < c - l: continue
        overlaps = True
      if overlaps: continue
      rows.append(row)
      cols.append(col)
      lengths.append(length)

  grid, output = common.grids(size, size)
  for row, col, length in zip(rows, cols, lengths):
    for r in range(row - length - 1, row + 2 * length + 1):
      for c in range(col - length - 1, col + 2 * length + 1):
        if r < row - 1 or r > row + length:  # skip the corners
          if c < col - 1 or c > col + length:
            continue
        output[r][c] = colors[1]
    for r in range(row - 1, row + length + 1):
      for c in range(col - 1, col + length + 1):
        grid[r][c] = colors[1]
        output[r][c] = colors[0]
    for r in range(row, row + length):
      for c in range(col, col + length):
        grid[r][c] = colors[0]
        output[r][c] = colors[1]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=10, rows=[4], cols=[4], lengths=[1], colors=[6, 4]),
      generate(size=10, rows=[4], cols=[4], lengths=[2], colors=[7, 2]),
      generate(size=10, rows=[4], cols=[3], lengths=[2], colors=[1, 3]),
  ]
  test = [
      generate(size=12, rows=[2, 7], cols=[2, 7], lengths=[1, 2],
               colors=[3, 8]),
  ]
  return {"train": train, "test": test}
