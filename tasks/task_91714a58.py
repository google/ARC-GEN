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


def generate(width=None, height=None, row=None, col=None, colors=None, size=16):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the box
    height: the height of the box
    row: the row of the box
    col: the column of the box
    colors: a list of digits representing the colors to be used
    size: the width and height of the (square) grid
  """
  if width is None:
    while True:
      width, height = common.randint(2, 8), common.randint(2, 8)
      if width * height >= 9 and width * height <= 16: break
    row = common.randint(1, size - height - 1)
    col = common.randint(1, size - width - 1)
    color = common.random_color()
    while True:
      pixels = common.random_pixels(size, size, 0.5)
      bitmap = common.grid(size, size)
      for r, c in pixels:
        bitmap[r][c] = common.random_color()
      # Make sure no two neighbors are the same color as our box.
      same_color_neighbors = False
      for r in range(size):
        for c in range(size):
          if bitmap[r][c] != color: continue
          for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            if common.get_pixel(bitmap, r + dr, c + dc) == color:
              same_color_neighbors = True
      if same_color_neighbors: continue
      # Now draw the box.
      for r in range(row, row + height):
        for c in range(col, col + width):
          bitmap[r][c] = color
      colors = []
      for r in bitmap:
        colors.extend(r)
      # Make sure no random pixels accidentally extend the box.
      all_alike = True
      for r in range(row, row + height):
        if colors[r * size + col - 1] != color: all_alike = False
      if all_alike: continue
      all_alike = True
      for r in range(row, row + height):
        if colors[r * size + col + width] != color: all_alike = False
      if all_alike: continue
      all_alike = True
      for c in range(col, col + width):
        if colors[(row - 1) * size + c] != color: all_alike = False
      if all_alike: continue
      all_alike = True
      for c in range(col, col + width):
        if colors[(row + height) * size + c] != color: all_alike = False
      if all_alike: continue
      break

  grid, output = common.grids(size, size)
  for r in range(size):
    for c in range(size):
      grid[r][c] = colors[r * size + c]
      if r < row or r >= row + height or c < col or c >= col + width: continue
      output[r][c] = grid[r][c]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=3, height=4, row=3, col=3,
               colors=[0, 0, 0, 0, 1, 1, 4, 0, 2, 0, 0, 0, 0, 2, 0, 5, 0, 0, 0,
                       3, 5, 0, 0, 0, 9, 9, 8, 0, 4, 0, 5, 8, 1, 0, 8, 2, 8, 0,
                       0, 6, 0, 8, 5, 0, 0, 0, 8, 0, 0, 0, 0, 2, 2, 2, 0, 0, 0,
                       0, 0, 6, 0, 0, 0, 0, 0, 0, 1, 2, 2, 2, 0, 0, 1, 9, 5, 0,
                       0, 2, 0, 4, 0, 4, 0, 2, 2, 2, 0, 2, 0, 0, 7, 0, 0, 0, 0,
                       0, 3, 0, 6, 2, 2, 2, 0, 0, 0, 3, 5, 0, 7, 0, 0, 0, 7, 0,
                       4, 6, 0, 0, 4, 7, 7, 3, 0, 2, 0, 0, 7, 1, 0, 7, 0, 0, 0,
                       0, 0, 9, 7, 7, 0, 0, 0, 8, 5, 2, 1, 5, 6, 4, 9, 3, 0, 3,
                       0, 0, 0, 0, 0, 9, 4, 6, 0, 2, 4, 0, 0, 0, 0, 0, 0, 0, 2,
                       0, 1, 6, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       2, 4, 0, 0, 6, 0, 0, 0, 0, 0, 6, 0, 0, 2, 0, 0, 0, 0, 0,
                       3, 0, 0, 7, 0, 2, 0, 7, 9, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0,
                       7, 0, 0, 0, 0, 0, 0, 0, 6, 5, 3, 0, 1, 0, 0, 9, 0, 0, 0,
                       2, 0, 0, 0, 1, 0, 0, 9, 0]),
      generate(width=7, height=2, row=11, col=2,
               colors=[0, 0, 7, 0, 0, 6, 0, 6, 0, 0, 0, 7, 3, 0, 0, 0, 0, 0, 3,
                       0, 0, 1, 0, 0, 8, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 3, 9,
                       0, 0, 0, 0, 0, 0, 0, 8, 0, 8, 2, 2, 0, 2, 9, 0, 0, 0, 0,
                       1, 0, 2, 0, 0, 0, 0, 0, 5, 2, 0, 0, 7, 0, 6, 0, 0, 0, 3,
                       0, 0, 1, 0, 4, 4, 0, 3, 9, 0, 0, 0, 0, 7, 0, 2, 0, 0, 0,
                       0, 8, 0, 0, 0, 0, 6, 0, 0, 0, 8, 0, 0, 3, 0, 0, 0, 0, 9,
                       0, 0, 0, 4, 8, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 9, 5, 0,
                       0, 0, 0, 4, 6, 0, 1, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       3, 1, 0, 8, 0, 5, 9, 4, 0, 9, 3, 9, 0, 3, 0, 0, 5, 6, 7,
                       0, 5, 0, 0, 0, 0, 0, 6, 6, 6, 6, 6, 6, 6, 0, 0, 0, 0, 7,
                       0, 0, 0, 4, 6, 6, 6, 6, 6, 6, 6, 0, 0, 4, 4, 6, 0, 2, 0,
                       5, 0, 0, 0, 0, 4, 5, 3, 0, 8, 0, 0, 0, 6, 9, 0, 0, 9, 7,
                       5, 0, 0, 0, 0, 0, 0, 0, 1, 0, 7, 1, 0, 8, 0, 0, 0, 0, 0,
                       1, 0, 3, 0, 0, 3, 8, 7, 0]),
      generate(width=3, height=3, row=2, col=8,
               colors=[3, 0, 0, 0, 0, 0, 6, 2, 0, 0, 0, 5, 0, 0, 0, 3, 0, 7, 0,
                       0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 8,
                       8, 0, 7, 7, 7, 0, 0, 0, 0, 4, 0, 2, 0, 0, 0, 0, 0, 0, 7,
                       7, 7, 0, 2, 0, 5, 0, 0, 8, 0, 0, 9, 6, 1, 7, 7, 7, 7, 0,
                       0, 0, 0, 0, 5, 0, 0, 0, 0, 3, 6, 0, 6, 0, 0, 3, 3, 0, 0,
                       0, 0, 4, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 9, 0,
                       0, 0, 0, 0, 0, 0, 0, 3, 0, 8, 0, 0, 0, 0, 0, 0, 3, 0, 0,
                       0, 0, 6, 0, 9, 0, 0, 0, 0, 0, 0, 9, 0, 0, 0, 1, 0, 0, 3,
                       0, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3,
                       3, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 5,
                       0, 0, 4, 0, 0, 1, 7, 0, 3, 0, 0, 7, 5, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 1, 7, 2, 0, 0, 5, 0, 0, 1, 0, 4, 0, 0, 0, 0,
                       0, 0, 0, 3, 0, 0, 2, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 7, 9,
                       0, 0, 0, 5, 0, 2, 0, 3, 0]),
  ]
  test = [
      generate(width=6, height=2, row=10, col=5,
               colors=[0, 0, 1, 7, 3, 0, 0, 0, 0, 0, 1, 2, 0, 4, 7, 0, 0, 0, 0,
                       3, 0, 0, 6, 8, 0, 0, 0, 0, 0, 0, 0, 0, 6, 0, 0, 8, 0, 1,
                       0, 0, 1, 0, 0, 0, 7, 0, 4, 8, 0, 3, 8, 0, 0, 0, 3, 0, 8,
                       0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 1, 0, 0, 8, 0, 0, 3, 8,
                       0, 0, 5, 0, 0, 8, 0, 0, 0, 0, 0, 0, 0, 0, 3, 7, 0, 0, 0,
                       0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 8, 0, 5, 0, 7, 0, 0,
                       0, 0, 0, 0, 0, 9, 0, 0, 2, 7, 0, 7, 0, 0, 9, 4, 0, 2, 1,
                       0, 0, 0, 0, 0, 7, 0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 1, 0, 0,
                       0, 0, 0, 0, 0, 0, 1, 5, 0, 8, 9, 4, 0, 5, 5, 5, 5, 5, 5,
                       3, 0, 0, 0, 0, 0, 0, 3, 0, 6, 5, 5, 5, 5, 5, 5, 0, 1, 4,
                       0, 0, 9, 5, 2, 0, 0, 5, 1, 3, 0, 0, 6, 2, 0, 0, 1, 5, 0,
                       7, 0, 0, 0, 0, 1, 6, 0, 7, 0, 3, 0, 6, 0, 0, 0, 0, 9, 0,
                       0, 3, 7, 7, 0, 6, 0, 0, 8, 0, 0, 0, 5, 0, 0, 0, 0, 0, 8,
                       0, 0, 0, 0, 0, 0, 0, 0, 9]),
  ]
  return {"train": train, "test": test}
