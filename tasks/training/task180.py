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


def generate(rows=None, cols=None, idxs=None, row_offsets=(0, 0, 1, 1),
             col_offsets=(0, 1, 0, 1), colors=(4, 5, 6, 9), size=4):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    idxs: a list of indices into the colors list
    row_offsets: a list of integers representing vertical offsets
    col_offsets: a list of integers representing horizontal offsets
    colors: digits representing the colors to be used
    size: the width and height of the (square) grid
  """
  if rows is None:
    rows, cols, idxs = [], [], []
    for idx in range(len(colors)):
      pixels = common.random_pixels(size, size)
      rows.extend([p[0] for p in pixels])
      cols.extend([p[1] for p in pixels])
      idxs.extend([idx] * len(pixels))

  grid, output = common.grid(2 * size, 2 * size), common.grid(size, size)
  for r, c, idx in zip(rows, cols, idxs):
    color = colors[idx]
    row_offset, col_offset = row_offsets[idx], col_offsets[idx]
    grid[size * row_offset + r][size * col_offset + c] = color
  for i in [0, 3, 2, 1]:
    for r, c, idx in zip(rows, cols, idxs):
      if idx != i: continue
      output[r][c] = colors[idx]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[0, 0, 1, 1, 2, 3, 0, 2, 3, 3, 0, 1, 1, 1, 2, 2, 2, 3, 3, 0,
                     1, 2, 2, 3],
               cols=[0, 1, 0, 1, 2, 1, 2, 2, 0, 1, 2, 0, 1, 2, 0, 2, 3, 1, 2, 2,
                     3, 0, 1, 0],
               idxs=[0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3,
                     3, 3, 3, 3]),
      generate(rows=[0, 0, 2, 2, 2, 3, 3, 3, 0, 0, 1, 1, 2, 3, 3, 3, 0, 1, 2, 2,
                     3, 3, 0, 0, 1, 2, 2, 3],
               cols=[0, 3, 0, 1, 3, 0, 2, 3, 0, 1, 2, 3, 1, 1, 2, 3, 3, 2, 0, 3,
                     2, 3, 1, 3, 1, 1, 3, 3],
               idxs=[0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2,
                     2, 2, 3, 3, 3, 3, 3, 3]),
      generate(rows=[0, 1, 2, 3, 3, 0, 1, 2, 3, 0, 1, 2, 2, 3, 3, 0, 0, 1, 1, 2,
                     2, 2],
               cols=[3, 0, 3, 1, 3, 0, 1, 2, 2, 0, 0, 0, 2, 0, 2, 1, 2, 1, 3, 0,
                     1, 2],
               idxs=[0, 0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3,
                     3, 3]),
      generate(rows=[0, 0, 1, 2, 2, 3, 0, 0, 1, 1, 2, 2, 3, 3, 0, 0, 0, 1, 1, 1,
                     2, 2, 3, 3, 3, 0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3],
               cols=[0, 3, 2, 2, 3, 0, 1, 3, 0, 3, 2, 3, 0, 3, 0, 1, 2, 0, 1, 2,
                     0, 3, 0, 1, 3, 0, 2, 3, 1, 2, 3, 0, 1, 3, 0, 2, 3],
               idxs=[0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2,
                     2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3]),
      generate(rows=[0, 0, 0, 1, 3, 0, 0, 0, 1, 1, 1, 2, 3, 0, 0, 0, 1, 2, 3, 3,
                     3, 0, 0, 1, 1, 2, 2, 2, 3, 3],
               cols=[1, 2, 3, 2, 0, 1, 2, 3, 0, 1, 3, 0, 0, 0, 1, 3, 3, 3, 0, 1,
                     3, 2, 3, 0, 2, 0, 2, 3, 1, 3],
               idxs=[0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2,
                     2, 3, 3, 3, 3, 3, 3, 3, 3, 3]),
  ]
  test = [
      generate(rows=[0, 0, 1, 1, 1, 2, 2, 2, 0, 1, 1, 1, 2, 2, 2, 3, 0, 0, 0, 1,
                     2, 3, 0, 0, 0, 1, 2, 2, 3],
               cols=[1, 3, 1, 2, 3, 0, 1, 2, 0, 0, 2, 3, 1, 2, 3, 0, 0, 2, 3, 3,
                     1, 0, 0, 1, 2, 1, 2, 3, 1],
               idxs=[0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2,
                     2, 2, 3, 3, 3, 3, 3, 3, 3]),
  ]
  return {"train": train, "test": test}
