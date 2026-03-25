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


def generate(size=None, rows=None, cols=None, color=None, boxrows=None,
             boxcols=None, wides=None, talls=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: the width and height of the (square) input grid
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    color: a digit representing a color to be used
    boxrows: a list of vertical coordinates where boxes should be placed
    boxcols: a list of horizontal coordinates where boxes should be placed
    wides: a list of widths of boxes
    talls: a list of heights of boxes
  """

  def draw(grid, output):
    for boxrow, boxcol, wide, tall in zip(boxrows, boxcols, wides, talls):
      for r in range(boxrow, boxrow + tall):
        for c in range(boxcol, boxcol + wide):
          output[r][c] = grid[r][c] = color
    # Only draw static if it doesn't connect two shapes.
    for r, c in zip(rows, cols):
      left = common.get_pixel(grid, r, c - 1)
      right = common.get_pixel(grid, r, c + 1)
      top = common.get_pixel(grid, r - 1, c)
      bottom = common.get_pixel(grid, r + 1, c)
      if (left <= 0 or right <= 0) and (top <= 0 or bottom <= 0):
        grid[r][c] = color
    # Check that no box touches more than one pixel directly.
    for boxrow, boxcol, wide, tall in zip(boxrows, boxcols, wides, talls):
      border = []
      for r in range(boxrow, boxrow + tall):
        border.append(common.get_pixel(grid, r, boxcol - 1))
        border.append(common.get_pixel(grid, r, boxcol + wide))
      for c in range(boxcol, boxcol + wide):
        border.append(common.get_pixel(grid, boxrow - 1, c))
        border.append(common.get_pixel(grid, boxrow + tall, c))
      if len([b for b in border if b == color]) > 1: return False
    return True

  if size is None:
    size, color = common.randint(7, 20), common.random_color()
    num_boxes = size // 3 - 1
    while True:
      wides = [common.randint(2, 5) for _ in range(num_boxes)]
      talls = [common.randint(2, 5) for _ in range(num_boxes)]
      boxrows = [common.randint(0, size - tall) for tall in talls]
      boxcols = [common.randint(0, size - wide) for wide in wides]
      if not common.overlaps(boxrows, boxcols, wides, talls, 1): break
    while True:
      pixels = common.random_pixels(size, size, 0.05)
      if not pixels: continue
      pixels = common.remove_neighbors(pixels)
      rows, cols = zip(*pixels)
      grid, output = common.grids(size, size)
      if not draw(grid, output): continue
      if grid != output: break

  grid, output = common.grids(size, size)
  draw(grid, output)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=13, rows=[0, 2, 5, 8, 10, 12], cols=[1, 4, 10, 1, 11, 4],
               color=7, boxrows=[0, 3, 8], boxcols=[8, 2, 8], wides=[5, 4, 3],
               talls=[3, 3, 2]),
      generate(size=17, rows=[1, 2, 2, 3, 4, 6, 9, 10, 12, 15, 16],
               cols=[12, 1, 6, 16, 4, 12, 13, 3, 7, 13, 10], color=6,
               boxrows=[2, 5, 10, 12], boxcols=[11, 3, 9, 2],
               wides=[3, 4, 5, 2], talls=[2, 3, 3, 3]),
      generate(size=7, rows=[0, 1, 4, 5, 6], cols=[1, 6, 5, 0, 5], color=5,
               boxrows=[2], boxcols=[1], wides=[4], talls=[3]),
  ]
  test = [
      generate(size=10, rows=[0, 1, 1, 3, 4, 5, 7, 8, 9, 9],
               cols=[9, 1, 7, 7, 0, 9, 0, 2, 4, 9], color=8, boxrows=[2, 5],
               boxcols=[1, 4], wides=[3, 5], talls=[2, 3]),
  ]
  return {"train": train, "test": test}
