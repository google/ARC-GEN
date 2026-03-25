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


def generate(size=None, length=None, row_offset=None, col_offset=None,
             rows=None, cols=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: The size of the grids.
    length: The length of the sides of the squares.
    row_offset: The row offset of the squares.
    col_offset: The col offset of the squares.
    rows: The row indices of the colors.
    cols: The col indices of the colors.
    colors: The colors of the squares.
  """

  def draw():
    grid, output = common.grids(size, size)
    for row in range(size):
      for col in range(size):
        if row % (length + 1) == length or col % (length + 1) == length:
          output[row][col] = grid[row][col] = 8
    for row, col, color in zip(rows, cols, colors):
      r, c = row_offset + row * (length + 1), col_offset + col * (length + 1)
      output[r][c] = grid[r][c] = color
    # First, decide the colors of the squares.
    upper = size // (length + 1)
    for row in range(upper):
      rr = row * (length + 1) + row_offset
      for j in range(upper):
        cj = j * (length + 1) + col_offset
        if not grid[rr][cj]: continue
        for i in range(j):
          ci = i * (length + 1) + col_offset
          if grid[rr][ci] != grid[rr][cj]: continue
          for k in range(i, j + 1):
            ck = k * (length + 1) + col_offset
            if output[rr][ck] and output[rr][ck] != grid[rr][cj]:
              output[rr][ck] = 6
            else:
              output[rr][ck] = grid[rr][cj]
    for col in range(upper):
      cc = col * (length + 1) + col_offset
      for j in range(upper):
        rj = j * (length + 1) + row_offset
        if not grid[rj][cc]: continue
        for i in range(j):
          ri = i * (length + 1) + row_offset
          if grid[ri][cc] != grid[rj][cc]: continue
          for k in range(i, j + 1):
            rk = k * (length + 1) + row_offset
            if output[rk][cc] and output[rk][cc] != grid[rj][cc]:
              output[rk][cc] = 6
            else:
              output[rk][cc] = grid[rj][cc]
    # Turn the pixels into squares.
    for row in range(upper):
      for col in range(upper):
        r, c = row * (length + 1), col * (length + 1)
        rr, cc = r + row_offset, c + col_offset
        common.rect(output, length, length, r, c, output[rr][cc])
    # Check that all the original colors are preserved.
    for row, col, color in zip(rows, cols, colors):
      r, c = row_offset + row * (length + 1), col_offset + col * (length + 1)
      if output[r][c] != color: return None, None
    return grid, output

  if size is None:
    size = common.randint(20, 28)
    length = common.randint(2, 5)
    upper = size // (length + 1)
    row_offset = common.randint(0, length - 1)
    col_offset = common.randint(0, length - 1)
    expect_pink = common.randint(0, 1)
    while True:
      good = True
      grid = common.grid(upper, upper)
      for color in [2, 3]:
        wide, tall = common.randint(3, upper), common.randint(3, upper)
        squish = common.randint(0, 2)
        if squish == 0: wide = 1
        if squish == 1: tall = 1
        brow = common.randint(0, upper - tall)
        bcol = common.randint(0, upper - wide)
        coords = [(brow, bcol)]
        if wide > 1: coords.append((brow, bcol + wide - 1))
        if tall > 1: coords.append((brow + tall - 1, bcol))
        if wide > 1 and tall > 1:
          coords.append((brow + tall - 1, bcol + wide - 1))
          # OK, sometimes we remove a corner, and sometimes we'll shift it.
          pos = common.randint(0, len(coords) - 1)
          if common.randint(0, 1):
            coords.pop(pos)
          else:
            r, c = coords[pos]
            if common.randint(0, 1):
              coords[pos] = (r, common.randint(0, upper - 1))
            else:
              coords[pos] = (common.randint(0, upper - 1), c)
        for r, c in coords:
          if grid[r][c] != 0: good = False
          grid[r][c] = color
      if not good: continue
      rows, cols, colors = [], [], []
      for r in range(upper):
        for c in range(upper):
          if not grid[r][c]: continue
          rows.append(r)
          cols.append(c)
          colors.append(grid[r][c])
      grid, output = draw()
      if not grid: continue
      if not expect_pink or 6 in common.flatten(output): break

  grid, output = draw()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=24, length=2, row_offset=0, col_offset=0,
               rows=[0, 1, 1, 4, 6, 6], cols=[3, 1, 6, 6, 3, 6],
               colors=[2, 3, 3, 2, 2, 2]),
      generate(size=22, length=3, row_offset=1, col_offset=1, rows=[0, 2, 2, 4],
               cols=[1, 0, 4, 1], colors=[2, 3, 3, 2]),
      generate(size=26, length=5, row_offset=2, col_offset=2,
               rows=[1, 1, 3, 3], cols=[0, 3, 0, 2], colors=[2, 2, 3, 3]),
  ]
  test = [
      generate(size=28, length=4, row_offset=1, col_offset=2,
               rows=[0, 1, 1, 3, 4], cols=[2, 0, 4, 0, 2],
               colors=[3, 2, 2, 2, 3]),
  ]
  return {"train": train, "test": test}
