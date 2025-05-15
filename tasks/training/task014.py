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


def generate(width=None, height=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the (square) grid
    height: the height of the (square) grid
    colors: a list of digits representing the colors to be used
  """
  if width is None:
    while True:
      width, height = common.randint(15, 25), common.randint(15, 25)
      rowthick, colthick = common.randint(2, 5), common.randint(2, 5)
      row = common.randint(5, height - 5 - rowthick)
      col = common.randint(5, width - 5 - colthick)
      color_list, quadrant = common.random_colors(2), common.randint(0, 3)
      grid = common.grid(width, height)
      for (r, c) in common.random_pixels(width, height, 0.9):
        quad = -1
        quad = 0 if r < row and c < col else quad
        quad = 1 if r < row and c >= col + colthick else quad
        quad = 2 if r >= row + rowthick and c < col else quad
        quad = 3 if r >= row + rowthick and c >= col + colthick else quad
        if quad == -1: continue
        grid[r][c] = color_list[0 if quad == quadrant else 1]
      colors = []
      for r in range(height):
        for c in range(width):
          colors.append(grid[r][c])
      foreground = [color for color in colors if color]
      rarest = min(set(foreground), key=foreground.count)
      if rarest == color_list[0]: break

  grid = common.grid(width, height)
  for r in range(height):
    for c in range(width):
      grid[r][c] = colors[r * width + c]
  foreground = [color for color in colors if color]
  rarest = min(set(foreground), key=foreground.count)
  min_row, min_col, max_row, max_col = height, width, -1, -1
  for r in range(height):
    for c in range(width):
      if grid[r][c] != rarest: continue
      min_row, min_col = min(min_row, r), min(min_col, c)
      max_row, max_col = max(max_row, r), max(max_col, c)
  output = common.grid(max_col - min_col + 1, max_row - min_row + 1)
  for r in range(min_row, max_row + 1):
    for c in range(min_col, max_col + 1):
      output[r - min_row][c - min_col] = grid[r][c]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=21, height=21,
               colors=[8, 8, 8, 8, 8, 0, 8, 8, 8, 8, 0, 0, 0, 0, 8, 8, 8, 8, 0,
                       8, 8, 8, 0, 0, 8, 0, 8, 0, 8, 8, 8, 0, 0, 0, 0, 8, 8, 8,
                       0, 0, 0, 8, 8, 8, 8, 0, 0, 0, 8, 8, 8, 8, 0, 0, 0, 0, 8,
                       8, 0, 8, 8, 8, 8, 8, 8, 0, 8, 8, 8, 8, 0, 8, 8, 0, 0, 0,
                       0, 8, 8, 0, 0, 0, 8, 8, 8, 8, 8, 8, 0, 8, 8, 0, 8, 8, 0,
                       0, 0, 0, 8, 8, 8, 0, 8, 8, 8, 0, 0, 0, 8, 8, 0, 8, 0, 0,
                       8, 0, 0, 0, 0, 8, 0, 0, 0, 8, 0, 0, 8, 8, 8, 8, 0, 0, 8,
                       0, 8, 0, 0, 0, 0, 0, 8, 8, 8, 0, 8, 8, 8, 8, 0, 0, 8, 0,
                       0, 8, 8, 0, 8, 0, 0, 0, 0, 8, 0, 8, 8, 8, 8, 8, 8, 8, 8,
                       8, 8, 8, 0, 8, 0, 0, 0, 0, 0, 0, 8, 8, 8, 8, 8, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 2, 2, 2, 0, 0, 2, 2, 2, 2, 0, 0, 0, 0, 8, 8,
                       0, 8, 8, 0, 8, 2, 0, 2, 2, 2, 0, 0, 2, 2, 2, 0, 0, 0, 0,
                       8, 8, 8, 8, 0, 8, 0, 0, 2, 2, 2, 2, 2, 2, 0, 2, 0, 0, 0,
                       0, 0, 8, 8, 8, 0, 0, 0, 8, 2, 2, 2, 2, 0, 2, 2, 2, 2, 2,
                       0, 0, 0, 0, 8, 8, 0, 8, 8, 8, 0, 2, 2, 2, 2, 2, 2, 0, 2,
                       0, 0, 0, 0, 0, 0, 8, 8, 8, 8, 8, 0, 0, 2, 2, 2, 2, 2, 0,
                       2, 0, 2, 2, 0, 0, 0, 0, 8, 0, 8, 0, 8, 8, 8, 2, 2, 0, 2,
                       2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 8, 0, 8, 0, 0, 8, 0, 2,
                       2, 0, 0, 2, 2, 0, 0, 2, 0, 0, 0, 0, 8, 0, 0, 0, 8, 8, 0,
                       2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 8, 8, 0, 0,
                       8, 8, 2, 0, 2, 2, 0, 2, 2, 2, 2, 2, 0, 0, 0, 0, 8, 8, 8,
                       0, 8, 8, 8]),
      generate(width=19, height=18,
               colors=[2, 0, 2, 2, 2, 2, 0, 0, 0, 0, 2, 0, 2, 2, 2, 2, 0, 0, 2,
                       2, 2, 2, 2, 0, 2, 2, 0, 0, 0, 0, 2, 2, 2, 2, 2, 0, 0, 0,
                       0, 0, 2, 2, 0, 2, 0, 0, 0, 0, 2, 2, 2, 0, 2, 2, 2, 2, 2,
                       2, 0, 2, 0, 2, 2, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 0, 0,
                       0, 2, 0, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 2, 2, 0, 2, 2, 2,
                       2, 2, 2, 0, 2, 0, 2, 0, 0, 0, 2, 0, 2, 2, 2, 2, 0, 2, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       2, 0, 2, 0, 0, 0, 2, 0, 0, 0, 0, 3, 3, 3, 3, 3, 0, 3, 3,
                       0, 2, 2, 0, 0, 2, 2, 0, 0, 0, 3, 3, 3, 0, 0, 0, 3, 3, 0,
                       0, 2, 2, 0, 0, 2, 0, 0, 0, 0, 3, 3, 3, 0, 3, 0, 3, 0, 0,
                       2, 2, 2, 0, 0, 2, 2, 0, 0, 0, 3, 3, 0, 0, 0, 3, 3, 3, 3,
                       2, 0, 0, 2, 2, 2, 0, 0, 0, 0, 3, 0, 0, 0, 3, 0, 3, 0, 3,
                       2, 0, 2, 0, 0, 0, 2, 0, 0, 0, 0, 3, 3, 0, 3, 3, 3, 0, 3,
                       0, 2, 2, 0, 2, 2, 0, 0, 0, 0, 0, 3, 3, 0, 0, 3, 0, 3,
                       0]),
      generate(width=17, height=19,
               colors=[0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0,
                       1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1,
                       1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1,
                       0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0,
                       1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1,
                       0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0,
                       0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4,
                       0, 0, 4, 0, 4, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 4, 4, 4,
                       4, 0, 4, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 4, 0, 4, 0, 0,
                       4, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 0, 4, 4, 4, 4, 0, 0,
                       0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 4, 4, 4, 0, 4, 4, 0, 0, 1,
                       1, 1, 1, 1, 1, 1, 1, 0, 0, 4, 4, 4, 4, 0, 0, 0, 0, 1, 0,
                       0, 0, 0, 1, 1, 1, 0, 4, 4, 4, 0, 4, 0, 0, 0, 1, 0, 1, 0,
                       1, 1, 1, 0, 0, 4, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1,
                       0, 1, 4, 4, 0, 4, 0, 4, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1,
                       0]),
  ]
  test = [
      generate(width=17, height=15,
               colors=[1, 1, 1, 1, 0, 1, 0, 0, 3, 0, 3, 3, 3, 3, 3, 3, 0, 1, 0,
                       1, 0, 1, 1, 0, 0, 0, 3, 0, 3, 3, 3, 0, 0, 0, 1, 1, 0, 1,
                       1, 0, 0, 0, 0, 0, 0, 3, 3, 3, 3, 0, 0, 0, 0, 0, 1, 1, 1,
                       0, 0, 3, 3, 0, 3, 3, 0, 3, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0,
                       0, 3, 0, 3, 3, 3, 0, 3, 3, 1, 1, 1, 1, 1, 1, 0, 0, 3, 3,
                       0, 0, 0, 3, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3,
                       0, 0, 0, 0, 3, 0, 0, 3, 3, 3, 0, 3, 0, 3, 0, 3, 0, 3, 3,
                       0, 0, 3, 0, 0, 0, 3, 0, 3, 3, 3, 0, 0, 0, 3, 3, 3, 3, 3,
                       0, 0, 0, 3, 0, 0, 0, 3, 0, 0, 0, 3, 3, 0, 3, 0, 3, 0, 0,
                       0, 0, 3, 3, 3, 3, 3, 3, 0, 3, 0, 3, 3, 0, 0, 0, 0, 0, 0,
                       0, 3, 3, 3, 0, 3, 3, 0]),
  ]
  return {"train": train, "test": test}
