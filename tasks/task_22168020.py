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


def generate(rows=None, cols=None, lengths=None, colors=None, size=10):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    lengths: a list of lengths
    colors: a list of digits representing the colors to be used
    size: the width and height of the (square) grid
  """
  if rows is None:
    rows, cols, lengths = [], [], []
    for _ in range(6):
      length = 2 * common.randint(2, 4)
      row = common.randint(0, size - length // 2 - 1)
      col = common.randint(0, size - length)
      overlaps = False
      for r, c, l in zip(rows, cols, lengths):
        if r + l // 2 < row or row + length // 2 < r: continue  # < on purpose!
        if c + l <= col or col + length <= c: continue
        overlaps = True
      if overlaps: continue
      rows.append(row)
      cols.append(col)
      lengths.append(length)
    colors = common.random_colors(len(lengths))

  grid, output = common.grids(size, size)
  for row, col, length, color in zip(rows, cols, lengths, colors):
    for idx in range(length):
      r = row + (idx if idx < length // 2 else length - idx - 1)
      grid[r][col + idx] = color
      while r >= row:
        output[r][col + idx] = color
        r -= 1
    for dc in range(2):
      grid[row + length // 2][col + length // 2 - 1 + dc] = color
      output[row + length // 2][col + length // 2 - 1 + dc] = color
    grid[row][col] = color
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[1], cols=[1], lengths=[8], colors=[3]),
      generate(rows=[2, 6], cols=[0, 4], lengths=[6, 6], colors=[1, 4]),
      generate(rows=[0, 5], cols=[0, 1], lengths=[6, 8], colors=[6, 8]),
  ]
  test = [
      generate(rows=[1, 2, 6], cols=[0, 4, 1], lengths=[4, 6, 6],
               colors=[4, 7, 3]),
  ]
  return {"train": train, "test": test}
