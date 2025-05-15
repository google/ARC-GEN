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


def generate(rows=None, cols=None, lengths=None, cdiffs=None, colors=None,
             size=10):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where diags should begin
    cols: a list of horizontal coordinates where diags should begin
    lengths: a list of lengths of the diags
    cdiffs: a list of +1 or -1 values representing the direction of the lines
    colors: a list of colors of the diags
    size: the width and height of the (square) grid
  """
  if rows is None:
    num_diags = common.randint(3, 6)
    rows, cols, lengths, cdiffs = [], [], [], []
    bitmap = common.grid(size, size)
    for _ in range(num_diags):
      max_length = common.randint(3, 7)
      row = common.randint(0, size - max_length)
      col = common.randint(0, size - max_length)
      cdiff = 2 * common.randint(0, 1) - 1  # will be -1 or 1
      col = col if cdiff > 0 else size - col - 1
      length = 0
      for i in range(max_length):
        r, c = row + i, col + i * cdiff
        if bitmap[r][c]: break
        if i and bitmap[r - 1][c] and bitmap[r][c - cdiff]: break
        length += 1
      if length < 3: continue
      for i in range(length):
        bitmap[row + i][col + i * cdiff] = 1
      rows.append(row)
      cols.append(col)
      lengths.append(length)
      cdiffs.append(cdiff)
    colors = common.random_colors(len(lengths))

  grid, output = common.grids(size, size)
  for r, c, length, cdiff, color in zip(rows, cols, lengths, cdiffs, colors):
    grid[r + length - 1][c + (length - 1) * cdiff] = grid[r][c] = color
    for i in range(length):
      output[r + i][c + i * cdiff] = color
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[0, 0, 5], cols=[2, 5, 3], lengths=[3, 5, 5],
               cdiffs=[-1, 1, 1], colors=[2, 6, 4]),
      generate(rows=[0, 0, 2, 5], cols=[0, 7, 6, 5], lengths=[4, 3, 6, 5],
               cdiffs=[1, 1, -1, 1], colors=[9, 3, 8, 7]),
      generate(rows=[0, 0, 2, 5], cols=[3, 5, 2, 4], lengths=[4, 5, 5, 5],
               cdiffs=[-1, 1, 1, -1], colors=[6, 8, 4, 9]),
  ]
  test = [
      generate(rows=[0, 0, 1, 4, 5], cols=[6, 9, 0, 0, 9], 
               lengths=[4, 4, 7, 4, 5], cdiffs=[-1, -1, 1, 1, -1],
               colors=[3, 9, 7, 6, 4]),
  ]
  return {"train": train, "test": test}
