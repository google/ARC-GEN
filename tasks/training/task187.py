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


def generate(width=None, height=None, rows=None, cols=None, wides=None,
             talls=None, lowerrows=None, lowercols=None, upperrows=None,
             uppercols=None, color=None, flip=None, xpose=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the grid
    height: the height of the grid
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    wides: a list of box widths
    talls: a list of box heights
    lowerrows: a list of lower vertical coordinates for lines
    lowercols: a list of lower horizontal coordinates for lines
    upperrows: a list of upper vertical coordinates for lines
    uppercols: a list of upper horizontal coordinates for lines
    color: the color of the lines
    flip: whether to flip the grids
    xpose: whether to transpose the grids
  """

  def draw(grid, output):
    legal = True
    # Draw and fill boxes.
    for row, col, wide, tall in zip(rows, cols, wides, talls):
      for r in range(row, row + tall):
        for c in range(col, col + wide):
          output[r][c] = grid[r][c] = color
      for r  in range(row + 1, row + tall - 1):
        for c in range(col + 1, col + wide - 1):
          grid[r][c] = common.black()
          output[r][c] = common.red()
    # Draw lines using -2 so we can detect intersection.
    for lrow, lcol, urow, ucol in zip(lowerrows, lowercols, upperrows,
                                      uppercols):
      dr, dc = (0 if lrow == urow else 1), (0 if lcol == ucol else 1)
      r, c = lrow, lcol
      if common.get_pixel(grid, r - dr, c - dc) == -2: legal = False
      while True:
        # Check for intersection.
        if common.get_pixel(grid, r, c) == -2: legal = False
        if common.get_pixel(grid, r + dr, c + dc) == -2: legal = False
        if grid[r][c] == 0: output[r][c] = grid[r][c] = -2
        if r == urow and c == ucol: break
        r, c = r + dr, c + dc
    # Redraw lines using the correct color.
    for r in range(height):
      for c in range(width):
        if grid[r][c] == -2: grid[r][c] = color
        if output[r][c] == -2: output[r][c] = color
    return legal

  if width is None:
    while True:  # Keep trying this until we get a grid with no intersections.
      width, height = common.randint(20, 25), common.randint(20, 25)
      wide0 = common.randint(6 * width // 15, 7 * width // 15)
      tall0 = common.randint(6 * height // 15, 7 * height // 15)
      wide1 = common.randint(6 * wide0 // 15, 7 * wide0 // 15)
      tall1 = common.randint(6 * tall0 // 15, 7 * tall0 // 15)
      wide2 = common.randint(6 * wide0 // 15, 7 * wide0 // 15)
      tall2 = common.randint(6 * tall0 // 15, 7 * tall0 // 15)
      wide3 = common.randint(6 * wide0 // 15, 7 * wide0 // 15)
      tall3 = common.randint(6 * tall0 // 15, 7 * tall0 // 15)
      row = common.randint(1, height - tall0 - tall1 - tall2 - 2)
      col = common.randint(1, width - wide0 - wide3 - 2)
      rows, cols, wides, talls = [], [], [], []
      # We always add the main box (0) and its little brother (1).
      rows.append(row + tall1 - 1)
      rows.append(row)
      cols.append(col)
      cols.append(col)
      wides.append(wide0)
      wides.append(wide1)
      talls.append(tall0)
      talls.append(tall1)
      # Only some of the time do we add the little sister (2) or the cousin (3).
      if common.randint(0, 1):
        rows.append(row + tall1 + tall0 - 2)
        cols.append(col + wide0 - wide2)
        wides.append(wide2)
        talls.append(tall2)
      if common.randint(0, 1):
        rows.append(row + tall1 - tall3)
        cols.append(col + wide0 - 1)
        wides.append(wide3)
        talls.append(tall3)
      # Add a bunch of random lines.
      lowerrows, lowercols, upperrows, uppercols = [], [], [], []
      for r, c, w, t in zip(rows, cols, wides, talls):
        lowerrows.append(r)
        upperrows.append(r)
        lowercols.append(max(0, c - common.randint(0, w - 1)))
        uppercols.append(min(width - 1, c + w + common.randint(0, w - 1)))
        lowerrows.append(r + t - 1)
        upperrows.append(r + t - 1)
        lowercols.append(max(0, c - common.randint(0, w - 1)))
        uppercols.append(min(width - 1, c + w + common.randint(0, w - 1)))
        lowerrows.append(max(0, r - common.randint(0, t)))
        upperrows.append(min(height - 1, r + t + common.randint(0, t - 1)))
        lowercols.append(c)
        uppercols.append(c)
        lowerrows.append(max(0, r - common.randint(0, t - 1)))
        upperrows.append(min(height - 1, r + t + common.randint(0, t - 1)))
        lowercols.append(c + w - 1)
        uppercols.append(c + w - 1)
      grid = common.grid(width, height)
      output = common.grid(width, height, common.green())
      if draw(grid, output): break
    color = common.random_color(exclude=[common.red(), common.green()])
    flip, xpose = common.randint(0, 1), common.randint(0, 1)

  grid = common.grid(width, height)
  output = common.grid(width, height, common.green())
  draw(grid, output)
  if flip: grid, output = grid[::-1], output[::-1]
  if xpose: grid, output = common.transpose(grid), common.transpose(output)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=23, height=23, rows=[4, 8, 15], cols=[6, 6, 13],
               wides=[5, 11, 4], talls=[5, 8, 5],
               lowerrows=[4, 8, 15, 19, 3, 0, 16, 1, 5],
               lowercols=[3, 3, 0, 12, 6, 10, 13, 16, 20],
               upperrows=[4, 8, 15, 19, 19, 10, 21, 21, 11],
               uppercols=[12, 21, 17, 20, 6, 10, 13, 16, 20], color=8, flip=0,
               xpose=0),
      generate(width=25, height=22, rows=[3, 3], cols=[4, 10], wides=[7, 7],
               talls=[10, 5],
               lowerrows=[3, 7, 12, 16, 1, 3, 1],
               lowercols=[0, 8, 1, 14, 4, 10, 16],
               upperrows=[3, 7, 12, 16, 18, 19, 19],
               uppercols=[24, 19, 12, 20, 4, 10, 16], color=1, flip=0, xpose=0),
      generate(width=21, height=24, rows=[5, 15, 15], cols=[4, 4, 13],
               wides=[10, 4, 6], talls=[11, 5, 4],
               lowerrows=[5, 8, 15, 18, 19, 1, 13, 2, 13],
               lowercols=[1, 9, 2, 12, 1, 4, 7, 13, 18],
               upperrows=[5, 8, 15, 18, 19, 22, 22, 22, 21],
               uppercols=[16, 17, 18, 20, 9, 4, 7, 13, 18], color=4, flip=0,
               xpose=0),
  ]
  test = [
      generate(width=25, height=22, rows=[4, 4], cols=[5, 16], wides=[12, 7],
               talls=[11, 6],
               lowerrows=[4, 9, 14, 17, 18, 1, 2, 1, 2],
               lowercols=[2, 10, 3, 12, 3, 5, 11, 16, 22],
               upperrows=[4, 9, 14, 17, 18, 21, 11, 19, 12],
               uppercols=[23, 23, 19, 20, 7, 5, 11, 16, 22], color=7, flip=0,
               xpose=0),
  ]
  return {"train": train, "test": test}
