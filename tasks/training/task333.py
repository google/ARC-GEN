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


def generate(rows=None, cols=None, colors=None, boxrow=None, boxcol=None,
             size=10):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    colors: a list of digits representing the colors to be used
    boxrow: the row where the box is placed
    boxcol: the column where the box is placed
    size: the width and height of the (square) grid
  """

  def draw(grid, output):
    for dr, dc in [(0, 0), (0, 1), (1, 0), (1, 1)]:
      grid[boxrow + dr][boxcol + dc] = common.green()
      output[boxrow + dr][boxcol + dc] = common.green()
    for row, col, color in zip(rows, cols, colors):
      output[row][col] = grid[row][col] = color
      if row in [boxrow, boxrow + 1]:
        c, dc = col, -1 if col > boxcol else 1
        while output[row][c + dc] != common.green():
          output[row][c + dc], c = color, c + dc
      if col in [boxcol, boxcol + 1]:
        r, dr = row, -1 if row > boxrow else 1
        while output[r + dr][col] != common.green():
          output[r + dr][col], r = color, r + dr
    for dr in range(-1, 3):
      for dc in range(-1, 3):
        if grid[boxrow + dr][boxcol + dc] in [common.black(), common.green()]:
          continue
        return False
    return True

  if rows is None:
    while True:
      boxrow, boxcol = common.randint(2, size - 3), common.randint(2, size - 3)
      color_list = common.random_colors(common.randint(1, 2),
                                        exclude=[common.green()])
      rows, cols, colors, up, down, left, right = [], [], [], 0, 0, 0, 0
      for color in color_list:
        for row, col in common.random_pixels(size, size, 0.05):
          if row in [boxrow, boxrow + 1]:
            if col < boxcol and not left:
              rows.append(row)
              cols.append(col)
              colors.append(color)
              left = 1
            if col > boxcol + 1 and not right:
              rows.append(row)
              cols.append(col)
              colors.append(color)
              right = 1
          elif col in [boxcol, boxcol + 1]:
            if row < boxrow and not up:
              rows.append(row)
              cols.append(col)
              colors.append(color)
              up = 1
            if row > boxrow + 1 and not down:
              rows.append(row)
              cols.append(col)
              colors.append(color)
              down = 1
          else:
            rows.append(row)
            cols.append(col)
            colors.append(color)
      grid, output = common.grids(size, size)
      if draw(grid, output): break

  grid, output = common.grids(size, size)
  draw(grid, output)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[0, 1, 3, 6, 7, 8, 9], cols=[0, 8, 8, 7, 6, 2, 4],
               colors=[1, 6, 1, 6, 6, 6, 1], boxrow=3, boxcol=2),
      generate(rows=[0, 0, 2, 2, 5, 6, 7, 8, 9, 9],
               cols=[1, 6, 3, 9, 1, 8, 3, 1, 5, 9],
               colors=[7, 8, 7, 8, 8, 8, 8, 7, 7, 7], boxrow=2, boxcol=5),
      generate(rows=[1, 2, 5, 9], cols=[4, 1, 9, 1], colors=[1, 1, 1, 1],
               boxrow=6, boxcol=4),
  ]
  test = [
      generate(rows=[0, 1, 2, 3, 4, 6, 8, 9, 9],
               cols=[3, 0, 7, 0, 7, 0, 7, 3, 5],
               colors=[2, 2, 2, 6, 6, 6, 2, 6, 6], boxrow=6, boxcol=2),
  ]
  return {"train": train, "test": test}
