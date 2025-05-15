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


def generate(colors=None, rows=None, cols=None, wides=None, talls=None, size=30,
             trisize=16):
  """Returns input and output grids according to the given parameters.

  Args:
    colors: a list of digits representing the colors to be used
    rows: a list of cutout rows
    cols: a list of cutout columns
    wides: a list of cutout widths
    talls: a list of cutout heights
    size: the width and height of the (square) grid
    trisize: the width and height of the triangle
  """

  def draw(grid, output):
    for row, col, wide, tall in zip(rows, cols, wides, talls):
      for r in range(row, row + tall):
        for c in range(col, col + wide):
          grid[r][c] = common.maroon()
    idx = 0
    for r in range(trisize):
      for c in range(r + 1):
        color = colors[idx]
        cells = [(r, c), (c, r), (r, 2 * trisize - c - 1),
                 (c, 2 * trisize - r - 1), (2 * trisize - r - 1, c),
                 (2 * trisize - c - 1, r),
                 (2 * trisize - r - 1, 2 * trisize - c - 1),
                 (2 * trisize - c - 1, 2 * trisize - r - 1)]
        # First, check that one is visible.
        shown = False
        for row, col in cells:
          if common.get_pixel(grid, row, col) not in [common.maroon(), -1]:
            shown = True
        if not shown: return False
        # Second, actually draw them.
        for row, col in cells:
          common.draw(output, row, col, color)
          if common.get_pixel(grid, row, col) == common.maroon(): continue
          common.draw(grid, row, col, color)
        idx += 1
    return True

  if colors is None:
    grid = common.grid(trisize, trisize)
    for _ in range(4 * size):
      row, col = common.randint(0, trisize - 1), common.randint(0, trisize - 1)
      color = common.random_color(exclude=[common.maroon()])
      common.draw(grid, row, col, color)
      if common.randint(0, 1): common.draw(grid, row + 1, col, color)
      if common.randint(0, 1): common.draw(grid, row, col + 1, color)
      if common.randint(0, 1): common.draw(grid, row + 1, col + 1, color)
    colors = []
    for r in range(trisize):
      for c in range(r + 1):
        colors.append(grid[r][c])
    num_cutouts = common.randint(2, 5)
    while True:
      wides = [common.randint(2, 8) for _ in range(num_cutouts)]
      talls = [common.randint(2, 8) for _ in range(num_cutouts)]
      cols = [common.randint(0, size - wide) for wide in wides]
      rows = [common.randint(0, size - tall) for tall in talls]
      grid, output = common.grids(size, size)
      if draw(grid, output): break

  grid, output = common.grids(size, size)
  draw(grid, output)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors=[0, 0, 0, 0, 0, 7, 0, 0, 7, 7, 0, 0, 0, 0, 0, 0, 5, 0, 0,
                       0, 0, 0, 0, 0, 7, 0, 0, 3, 0, 0, 7, 0, 0, 0, 0, 0, 6, 6,
                       5, 5, 0, 1, 0, 0, 0, 6, 6, 5, 0, 1, 0, 0, 7, 0, 8, 5, 5,
                       4, 0, 0, 0, 0, 0, 4, 0, 0, 5, 0, 0, 4, 0, 7, 0, 2, 0, 0,
                       5, 0, 0, 1, 0, 0, 7, 0, 4, 0, 0, 0, 0, 0, 1, 1, 0, 0, 7,
                       0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 8, 0, 0,
                       0, 0, 7, 0, 1, 1, 0, 7, 0, 2, 0, 0, 0, 0, 0, 0, 7, 0, 1,
                       1, 0, 1],
               rows=[5, 5, 8, 9], cols=[22, 28, 0, 12], wides=[6, 2, 7, 7],
               talls=[8, 6, 3, 6]),
      generate(colors=[3, 0, 0, 0, 0, 7, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3,
                       0, 0, 0, 0, 4, 0, 1, 1, 0, 0, 3, 0, 0, 1, 1, 2, 2, 0, 8,
                       3, 3, 1, 0, 8, 0, 0, 8, 0, 3, 0, 0, 1, 0, 0, 0, 8, 3, 3,
                       4, 4, 8, 0, 6, 6, 1, 0, 2, 3, 0, 4, 0, 0, 0, 6, 6, 0, 0,
                       2, 0, 1, 0, 8, 0, 3, 0, 8, 0, 0, 5, 7, 0, 0, 0, 1, 0, 0,
                       0, 3, 0, 0, 5, 0, 0, 7, 5, 5, 8, 0, 6, 6, 8, 0, 1, 1, 7,
                       0, 0, 7, 0, 0, 0, 0, 0, 6, 6, 0, 0, 1, 0, 0, 7, 7, 0, 0,
                       0, 0, 8],
               rows=[1, 16, 18, 25, 28], cols=[21, 9, 21, 20, 17],
               wides=[5, 2, 2, 6, 7], talls=[4, 2, 3, 2, 2]),
      generate(colors=[0, 5, 0, 0, 0, 0, 0, 0, 1, 1, 0, 5, 0, 0, 1, 5, 0, 0, 0,
                       0, 1, 0, 0, 4, 4, 0, 0, 1, 0, 0, 4, 0, 0, 0, 0, 1, 8, 8,
                       0, 4, 4, 4, 0, 0, 2, 8, 0, 4, 4, 4, 4, 0, 3, 2, 0, 0, 4,
                       2, 0, 0, 0, 8, 8, 1, 0, 3, 4, 4, 0, 0, 0, 3, 8, 0, 0, 0,
                       0, 3, 4, 4, 0, 0, 8, 8, 0, 7, 4, 0, 5, 0, 0, 4, 4, 0, 3,
                       8, 8, 7, 7, 0, 0, 0, 5, 6, 6, 0, 0, 8, 8, 0, 7, 0, 5, 5,
                       0, 0, 6, 7, 0, 2, 0, 3, 8, 0, 7, 7, 5, 0, 0, 5, 6, 0, 0,
                       7, 0, 2],
               rows=[0, 7], cols=[17, 0], wides=[4, 3], talls=[7, 7]),
      generate(colors=[0, 0, 7, 0, 1, 5, 1, 0, 0, 5, 7, 0, 6, 0, 8, 0, 7, 0, 0,
                       8, 0, 6, 0, 0, 0, 6, 0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0,
                       0, 6, 3, 3, 0, 2, 0, 0, 4, 6, 6, 3, 0, 2, 0, 8, 8, 0, 6,
                       3, 3, 0, 2, 7, 7, 1, 1, 0, 6, 6, 3, 3, 2, 0, 7, 0, 1, 1,
                       0, 0, 3, 3, 0, 2, 4, 4, 1, 0, 7, 7, 0, 2, 0, 3, 0, 2, 0,
                       4, 4, 0, 0, 7, 0, 2, 2, 2, 0, 0, 2, 7, 7, 1, 0, 0, 0, 0,
                       2, 4, 4, 0, 2, 6, 2, 0, 7, 0, 0, 0, 0, 4, 2, 2, 4, 0, 2,
                       2, 6, 0],
               rows=[4, 7, 11, 11, 23], cols=[9, 27, 5, 8, 9],
               wides=[3, 3, 3, 5, 2], talls=[3, 4, 7, 4, 7]),
  ]
  test = [
      generate(colors=[8, 0, 8, 7, 0, 2, 0, 0, 0, 0, 7, 7, 1, 1, 0, 7, 7, 1, 1,
                       0, 5, 1, 1, 0, 8, 0, 6, 2, 1, 1, 8, 0, 6, 6, 0, 2, 0, 3,
                       0, 6, 0, 8, 0, 0, 0, 3, 3, 6, 6, 8, 8, 0, 0, 0, 6, 0, 6,
                       7, 7, 0, 0, 0, 6, 0, 0, 0, 6, 6, 7, 7, 0, 0, 6, 0, 0, 5,
                       0, 0, 0, 8, 0, 0, 6, 6, 0, 0, 6, 0, 3, 0, 0, 8, 8, 0, 0,
                       6, 6, 0, 0, 0, 0, 0, 3, 4, 0, 0, 0, 0, 6, 0, 0, 5, 5, 3,
                       0, 0, 6, 3, 0, 2, 0, 0, 6, 0, 0, 0, 5, 0, 0, 3, 6, 6, 0,
                       0, 0, 2],
               rows=[2, 3, 7, 27], cols=[0, 20, 22, 18], wides=[7, 5, 5, 7],
               talls=[3, 5, 5, 2]),
  ]
  return {"train": train, "test": test}
