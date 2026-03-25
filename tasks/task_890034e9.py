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


def generate(width=None, height=None, rows=None, cols=None, boxcolor=None,
    colors=None, size=21,
):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the cutouts
    height: the height of the cutouts
    rows: a list of vertical coordinates where cutouts should be placed
    cols: a list of horizontal coordinates where cutouts should be placed
    boxcolor: the color of the boxes
    colors: a list of digits representing the colors to be used
    size: the width and height of the (square) grid
  """

  def draw(grid, output):
    for r in range(size):
      for c in range(size):
        output[r][c] = grid[r][c] = colors[r * size + c]
    for idx in range(len(rows)):
      row, col = rows[idx], cols[idx]
      for r in range(row - 1, row + height + 1):
        output[r][col - 1] = output[r][col + width] = boxcolor
        if idx > 0: continue
        grid[r][col - 1] = grid[r][col + width] = boxcolor
      for c in range(col - 1, col + width + 1):
        output[row - 1][c] = output[row + height][c] = boxcolor
        if idx > 0: continue
        grid[row - 1][c] = grid[row + height][c] = boxcolor
    # Check if there are any holes that we didn't mean to create.
    boxes = list(zip(rows, cols))
    for row in range(size):
      for col in range(size):
        if (row, col) in boxes: continue
        hole = True
        for r in range(height):
          for c in range(width):
            if common.get_pixel(grid, row + r, col + c) != common.black():
              hole = False
        if hole: return False
    return True


  if width is None:
    while True:
      width, height = common.randint(2, 5), common.randint(2, 5)
      if width > 2 or height > 2: break  # We don't want a tiny 2x2 box.
    color_list = common.random_colors(3)
    while True:
      boxcolor, colors = color_list[0], []
      for _ in range(size * size):
        idx = common.randint(0, 9)
        if not idx:  # Only very rarely add background pixels
          colors.append(common.black())
          continue
        colors.append(color_list[common.randint(1, 2)])
      while True:
        rows = [common.randint(2, size - height - 2) for _ in range(2)]
        cols = [common.randint(2, size - width - 2) for _ in range(2)]
        if rows[0] + height + 2 < rows[1] or rows[1] + height + 2 < rows[0]:
          break
        if cols[0] + width + 2 < cols[1] or cols[1] + width + 2 < cols[0]: break
      for row, col in zip(rows, cols):
        for r in range(row, row + height):
          for c in range(col, col + width):
            colors[r * size + c] = common.black()
      grid, output = common.grids(size, size)
      if draw(grid, output): break

  grid, output = common.grids(size, size)
  draw(grid, output)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=2, height=3, rows=[3, 14], cols=[7, 10], boxcolor=2,
               colors=[0, 8, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1,
                       1, 1, 1, 1, 0, 8, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0,
                       1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 2, 2, 2, 2, 1, 1, 1, 1, 1,
                       8, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 2, 0, 0, 2, 1, 1, 1,
                       1, 1, 1, 1, 8, 1, 0, 1, 1, 1, 1, 1, 1, 0, 2, 0, 0, 2, 1,
                       0, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 2, 0, 0,
                       2, 1, 8, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 2,
                       2, 2, 2, 1, 0, 1, 0, 0, 1, 1, 8, 0, 0, 8, 0, 1, 8, 0, 0,
                       1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 8, 1, 1, 0, 0, 1, 1, 1,
                       8, 8, 1, 1, 1, 0, 0, 8, 1, 1, 1, 1, 1, 8, 1, 0, 0, 1, 8,
                       1, 0, 1, 1, 1, 1, 0, 8, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0,
                       1, 8, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 8, 1,
                       1, 8, 1, 1, 1, 1, 8, 1, 0, 1, 1, 8, 1, 0, 1, 1, 1, 0, 1,
                       1, 1, 1, 0, 1, 1, 0, 8, 1, 1, 8, 0, 1, 1, 1, 1, 1, 1, 1,
                       0, 1, 0, 8, 1, 1, 1, 1, 1, 8, 1, 1, 1, 0, 1, 0, 0, 1, 1,
                       0, 8, 1, 0, 1, 0, 1, 1, 8, 1, 1, 1, 1, 1, 1, 0, 0, 8, 1,
                       0, 0, 1, 1, 8, 1, 1, 8, 1, 0, 1, 8, 8, 8, 1, 1, 1, 1, 8,
                       1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 8, 0,
                       0, 8, 1, 1, 0, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 8, 8, 1,
                       1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1,
                       8, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 1,
                       1, 1, 0, 0, 8, 1, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 8, 0, 0,
                       0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 0,
                       8, 1, 8, 0]),
      generate(width=3, height=2, rows=[11, 8], cols=[4, 12], boxcolor=8,
               colors=[3, 0, 3, 4, 3, 3, 3, 3, 0, 3, 3, 4, 0, 3, 0, 4, 3, 4, 4,
                       0, 0, 3, 3, 0, 0, 3, 3, 3, 4, 0, 0, 4, 4, 4, 3, 0, 0, 3,
                       3, 4, 0, 3, 4, 4, 4, 3, 4, 3, 0, 3, 0, 0, 4, 3, 0, 3, 3,
                       4, 3, 0, 0, 3, 0, 0, 4, 4, 4, 3, 0, 3, 3, 3, 0, 3, 0, 3,
                       0, 0, 0, 0, 3, 4, 3, 3, 3, 3, 0, 4, 3, 3, 0, 0, 0, 0, 3,
                       0, 4, 4, 4, 3, 0, 3, 0, 0, 0, 0, 3, 0, 0, 3, 0, 0, 3, 0,
                       3, 0, 0, 0, 3, 3, 3, 3, 4, 3, 0, 3, 0, 3, 0, 0, 3, 4, 0,
                       3, 4, 0, 4, 4, 0, 0, 3, 4, 0, 0, 0, 3, 3, 0, 3, 3, 3, 0,
                       4, 4, 3, 4, 3, 0, 3, 3, 3, 4, 0, 3, 0, 3, 3, 3, 4, 0, 4,
                       3, 4, 3, 4, 4, 0, 0, 4, 0, 0, 0, 0, 3, 0, 3, 3, 0, 0, 0,
                       0, 4, 0, 0, 0, 0, 3, 4, 4, 3, 4, 0, 0, 0, 4, 0, 0, 4, 3,
                       3, 3, 0, 0, 8, 8, 8, 8, 8, 4, 3, 0, 3, 3, 0, 4, 4, 0, 4,
                       4, 4, 4, 3, 3, 0, 8, 0, 0, 0, 8, 3, 0, 0, 0, 0, 4, 0, 3,
                       3, 0, 4, 3, 3, 0, 0, 0, 8, 0, 0, 0, 8, 3, 3, 0, 3, 3, 4,
                       3, 0, 4, 0, 3, 0, 0, 3, 0, 4, 8, 8, 8, 8, 8, 0, 3, 0, 3,
                       0, 0, 3, 3, 3, 0, 4, 3, 0, 4, 0, 0, 0, 0, 3, 0, 4, 0, 0,
                       3, 0, 0, 3, 3, 3, 4, 0, 4, 0, 3, 0, 0, 4, 3, 0, 0, 0, 3,
                       0, 0, 3, 4, 0, 0, 4, 0, 0, 3, 4, 3, 4, 4, 4, 0, 0, 3, 0,
                       3, 4, 4, 3, 4, 3, 4, 0, 4, 4, 0, 3, 4, 3, 4, 3, 4, 3, 3,
                       0, 0, 0, 0, 3, 0, 3, 4, 0, 0, 0, 3, 3, 3, 3, 0, 3, 0, 0,
                       0, 0, 0, 3, 0, 3, 3, 4, 0, 3, 3, 3, 4, 0, 4, 0, 3, 4, 0,
                       3, 3, 3, 0, 4, 0, 4, 3, 0, 0, 0, 3, 0, 0, 3, 3, 0, 0, 4,
                       3, 0, 0, 4, 3, 3, 3, 0, 4, 4, 3, 4, 3, 4, 0, 4, 3, 4, 4,
                       0, 0, 4, 0]),
      generate(width=4, height=3, rows=[4, 15], cols=[5, 11], boxcolor=4,
               colors=[0, 0, 3, 0, 3, 2, 0, 2, 0, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2,
                       3, 3, 3, 2, 2, 0, 3, 2, 0, 2, 2, 2, 2, 2, 2, 2, 2, 3, 2,
                       2, 0, 3, 2, 3, 3, 0, 3, 0, 0, 3, 2, 2, 2, 2, 3, 2, 2, 2,
                       2, 3, 0, 0, 3, 2, 2, 2, 3, 2, 4, 4, 4, 4, 4, 4, 3, 0, 3,
                       2, 0, 2, 2, 2, 0, 0, 3, 3, 3, 2, 0, 4, 0, 0, 0, 0, 4, 2,
                       0, 2, 2, 0, 2, 3, 0, 2, 2, 0, 3, 2, 2, 2, 4, 0, 0, 0, 0,
                       4, 0, 3, 2, 2, 3, 2, 2, 3, 3, 2, 0, 2, 0, 2, 0, 4, 0, 0,
                       0, 0, 4, 2, 0, 0, 0, 2, 2, 2, 0, 2, 2, 2, 0, 2, 0, 2, 4,
                       4, 4, 4, 4, 4, 2, 2, 0, 2, 0, 2, 0, 0, 2, 2, 2, 2, 0, 2,
                       2, 2, 0, 2, 0, 2, 0, 3, 2, 3, 3, 0, 2, 0, 0, 0, 2, 2, 0,
                       2, 3, 0, 3, 0, 2, 3, 2, 2, 2, 0, 2, 0, 0, 0, 2, 2, 3, 2,
                       0, 3, 0, 2, 0, 2, 0, 0, 2, 2, 0, 3, 3, 2, 3, 0, 3, 3, 0,
                       0, 3, 0, 2, 3, 0, 3, 2, 2, 2, 2, 2, 0, 0, 0, 0, 2, 0, 2,
                       0, 3, 0, 0, 2, 3, 2, 2, 0, 2, 0, 2, 2, 0, 3, 2, 2, 2, 2,
                       3, 0, 2, 2, 2, 2, 2, 3, 3, 3, 2, 0, 2, 0, 2, 0, 3, 2, 2,
                       2, 0, 0, 3, 2, 2, 3, 2, 2, 0, 0, 2, 2, 2, 3, 2, 0, 0, 2,
                       3, 2, 0, 3, 0, 2, 2, 3, 2, 2, 0, 2, 2, 2, 2, 2, 3, 2, 3,
                       3, 3, 2, 0, 0, 0, 0, 2, 0, 0, 2, 3, 0, 2, 2, 2, 2, 3, 0,
                       0, 3, 3, 2, 0, 0, 0, 0, 0, 0, 2, 2, 3, 2, 0, 2, 0, 3, 2,
                       2, 2, 3, 2, 3, 3, 3, 0, 0, 0, 0, 0, 2, 0, 0, 2, 3, 2, 2,
                       0, 0, 0, 0, 0, 0, 0, 3, 2, 3, 2, 2, 3, 0, 0, 2, 2, 0, 0,
                       0, 3, 0, 2, 2, 2, 0, 0, 0, 2, 2, 2, 2, 3, 0, 2, 0, 0, 0,
                       3, 2, 2, 3, 2, 2, 2, 0, 0, 3, 2, 0, 3, 2, 0, 2, 2, 2, 3,
                       0, 0, 2, 2]),
  ]
  test = [
      generate(width=2, height=5, rows=[14, 4], cols=[2, 13], boxcolor=3,
               colors=[0, 2, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 1, 2, 0, 1, 1, 1, 0,
                       1, 2, 1, 1, 1, 0, 2, 1, 2, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1,
                       0, 2, 1, 1, 1, 1, 1, 0, 2, 2, 1, 1, 1, 1, 1, 0, 1, 1, 1,
                       0, 1, 1, 2, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1,
                       1, 1, 2, 0, 1, 1, 1, 1, 0, 2, 1, 0, 1, 1, 2, 2, 1, 1, 0,
                       1, 1, 0, 0, 1, 0, 1, 1, 1, 2, 1, 0, 0, 1, 1, 0, 1, 1, 1,
                       1, 1, 0, 1, 0, 0, 1, 1, 0, 0, 2, 0, 0, 1, 1, 0, 0, 0, 1,
                       1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 2, 2,
                       1, 0, 1, 2, 2, 1, 1, 2, 0, 0, 1, 0, 1, 1, 1, 2, 1, 0, 1,
                       0, 1, 0, 0, 2, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0,
                       1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0,
                       1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1,
                       1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0,
                       0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0,
                       0, 2, 1, 1, 1, 1, 1, 1, 3, 3, 3, 3, 1, 2, 0, 2, 1, 1, 0,
                       1, 0, 0, 1, 0, 0, 1, 1, 1, 2, 3, 0, 0, 3, 1, 0, 1, 0, 1,
                       0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 3, 0, 0, 3, 1, 1, 2,
                       0, 1, 1, 1, 0, 2, 1, 1, 1, 0, 1, 1, 1, 1, 3, 0, 0, 3, 1,
                       2, 0, 0, 0, 1, 2, 1, 1, 1, 2, 1, 0, 1, 0, 1, 1, 3, 0, 0,
                       3, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 3,
                       0, 0, 3, 1, 0, 2, 0, 1, 1, 1, 1, 0, 1, 1, 0, 2, 1, 1, 1,
                       1, 3, 3, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1,
                       1, 0, 1, 1, 1, 2, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0,
                       1, 1, 1, 1]),
  ]
  return {"train": train, "test": test}
