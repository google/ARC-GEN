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


def generate(rows=None, cols=None, idxs=None, colors=None, size=30):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    idxs: a list of indices into the colors list
    colors: a list of digits representing colors to be used (0th is special!)
    size: the width and height of the (square) grid
  """
  if rows is None:
    # First, create the pixels for our little celestial object (color idx is 0).
    rows, cols, idxs = [], [], []
    width, height = common.randint(3, 5), common.randint(3, 5)
    row = common.randint(5, size - height - 5)
    col = common.randint(5, size - width - 5)
    while True:
      pixels = common.random_pixels(width, height, 0.75)
      if common.connected(pixels): break
    for r in range(height):
      for c in range(width):
        if (r, c) not in pixels: continue
        rows.append(row + r)
        cols.append(col + c)
        idxs.append(0)
    colors = common.random_colors(common.randint(2, 4))
    # Then, create all the other pixels in the background (but don't clobber!).
    pixels = common.random_pixels(size, size, (len(colors) - 1) / 50)
    for (r, c) in pixels:
      if r < row - 1 or r > row + height or c < col - 1 or c > col + width:
        rows.append(r)
        cols.append(c)
        idxs.append(common.randint(1, len(colors) - 1))

  min_col = min(col for col, idx in zip(cols, idxs) if idx == 0)
  max_col = max(col for col, idx in zip(cols, idxs) if idx == 0)
  min_row = min(row for row, idx in zip(rows, idxs) if idx == 0)
  max_row = max(row for row, idx in zip(rows, idxs) if idx == 0)
  grid = common.grid(size, size)
  output = common.grid(max_col - min_col + 1, max_row - min_row + 1)
  for r, c, idx in zip(rows, cols, idxs):
    grid[r][c] = colors[idx]
    if r < min_row or r > max_row or c < min_col or c > max_col: continue
    output[r - min_row][c - min_col] = colors[idx]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[0, 0, 0, 1, 2, 2, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 5, 5, 6, 6,
                     7, 7, 8, 8, 8, 8, 8, 8, 8, 8, 8, 9, 9, 10, 10, 10, 11, 11,
                     11, 11, 11, 11, 11, 11, 11, 11, 12, 12, 12, 13, 13, 13, 13,
                     13, 14, 14, 14, 14, 14, 15, 15, 16, 16, 16, 16, 17, 17, 18,
                     18, 18, 19, 19, 19, 19, 19, 19, 20, 20, 20, 21, 22, 22, 23,
                     23, 23, 23, 23, 24, 24, 25, 25, 26, 26, 26, 26, 27, 27, 27,
                     28, 28, 28, 28, 29, 29],
               cols=[0, 5, 22, 15, 10, 26, 8, 15, 22, 3, 4, 8, 12, 13, 15, 19,
                     18, 29, 4, 7, 4, 24, 2, 4, 11, 15, 17, 18, 19, 21, 27, 0,
                     9, 17, 18, 21, 0, 2, 5, 13, 14, 17, 18, 19, 25, 28, 17, 19,
                     22, 15, 17, 18, 19, 27, 3, 7, 11, 18, 19, 0, 28, 8, 12, 22,
                     29, 19, 21, 1, 7, 25, 4, 13, 15, 20, 22, 29, 1, 16, 23, 4,
                     23, 24, 0, 12, 21, 24, 29, 7, 15, 20, 22, 13, 24, 26, 29,
                     7, 8, 25, 13, 17, 21, 25, 6, 10],
               idxs=[1, 1, 2, 2, 2, 1, 2, 2, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 2, 1,
                     2, 1, 2, 1, 2, 1, 1, 2, 1, 2, 1, 2, 1, 0, 0, 1, 2, 2, 1, 1,
                     1, 0, 0, 0, 1, 1, 0, 0, 2, 1, 0, 0, 0, 2, 2, 2, 2, 0, 0, 2,
                     1, 1, 2, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1, 2, 1, 1,
                     1, 2, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 2, 1, 1, 2, 2, 2,
                     2, 2, 2, 1],
               colors=[3, 1, 5]),
      generate(rows=[0, 0, 0, 1, 2, 2, 2, 3, 3, 3, 3, 4, 5, 5, 6, 7, 7, 8, 9, 9,
                     9, 10, 10, 10, 10, 11, 11, 11, 12, 12, 13, 14, 17, 17, 18,
                     19, 19, 20, 20, 21, 23, 23, 25, 25, 26, 27, 27, 27, 28],
               cols=[10, 11, 23, 6, 0, 7, 10, 0, 2, 7, 27, 13, 2, 7, 7, 20, 27,
                     20, 7, 12, 23, 11, 12, 13, 22, 3, 12, 13, 6, 29, 29, 8, 19,
                     25, 28, 1, 16, 8, 28, 19, 2, 6, 4, 14, 6, 17, 18, 21, 27],
               idxs=[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0,
                     1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                     1, 1, 1, 1, 1, 1, 1, 1, 1],
               colors=[4, 2]),
  ]
  test = [
      generate(rows=[0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 3, 3, 3,
                     3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 5, 5, 6, 6, 6, 6, 6, 6, 6, 6,
                     7, 7, 7, 7, 7, 8, 8, 8, 8, 8, 10, 10, 11, 11, 11, 11, 11,
                     11, 12, 12, 12, 12, 12, 12, 12, 13, 13, 13, 13, 13, 13, 14,
                     14, 14, 14, 15, 15, 15, 15, 15, 15, 15, 15, 16, 16, 16, 17,
                     17, 18, 18, 18, 19, 19, 19, 19, 19, 19, 20, 20, 21, 21, 21,
                     22, 22, 22, 22, 23, 23, 23, 23, 23, 23, 24, 24, 24, 24, 24,
                     24, 24, 25, 25, 25, 25, 25, 25, 25, 26, 26, 26, 27, 27, 27,
                     27, 27, 27, 28, 28, 29, 29, 29, 29, 29],
               cols=[2, 4, 6, 19, 21, 2, 3, 17, 20, 27, 28, 0, 19, 20, 21, 22,
                     23, 2, 9, 12, 16, 20, 23, 29, 0, 16, 23, 24, 26, 29, 17,
                     29, 1, 3, 8, 9, 22, 26, 27, 29, 3, 4, 18, 19, 22, 11, 16,
                     18, 22, 25, 5, 20, 1, 2, 5, 10, 11, 17, 3, 6, 10, 12, 20,
                     21, 22, 2, 10, 19, 20, 22, 26, 8, 19, 20, 22, 3, 12, 17,
                     20, 21, 22, 24, 25, 0, 13, 15, 10, 11, 4, 9, 17, 2, 8, 17,
                     18, 22, 29, 17, 19, 8, 17, 25, 6, 12, 14, 29, 10, 14, 16,
                     18, 21, 26, 6, 8, 11, 12, 13, 17, 25, 1, 12, 16, 20, 23,
                     25, 27, 2, 5, 7, 5, 14, 17, 19, 20, 22, 16, 21, 2, 7, 17,
                     21, 29],
               idxs=[1, 2, 3, 2, 3, 3, 2, 3, 3, 1, 1, 1, 3, 3, 3, 1, 2, 3, 3, 1,
                     3, 2, 2, 3, 1, 2, 1, 3, 3, 2, 3, 3, 3, 1, 1, 1, 3, 3, 3, 2,
                     1, 3, 2, 1, 3, 1, 3, 2, 3, 2, 1, 3, 1, 3, 2, 3, 2, 3, 1, 1,
                     2, 2, 0, 0, 0, 1, 3, 0, 0, 0, 1, 1, 0, 0, 0, 2, 1, 2, 0, 0,
                     0, 3, 2, 1, 2, 3, 1, 1, 3, 2, 3, 3, 2, 3, 2, 2, 2, 1, 2, 2,
                     1, 1, 3, 2, 1, 2, 1, 2, 2, 1, 2, 3, 3, 3, 1, 1, 1, 3, 1, 3,
                     3, 3, 1, 3, 2, 2, 1, 2, 1, 2, 1, 3, 2, 1, 1, 2, 2, 3, 3, 2,
                     2, 2],
               colors=[2, 1, 3, 8]),
  ]
  return {"train": train, "test": test}
