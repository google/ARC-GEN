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


def generate(width=None, height=None, rows=None, cols=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the input grid.
    height: The height of the input grid.
    rows: The rows of the pixels.
    cols: The columns of the pixels.
    colors: The colors of the pixels.
  """

  def draw():
    grid, output = common.grids(width, height)
    for row, col, color in zip(rows, cols, colors):
      if color == 5: output[row][col] = grid[row][col] = color
    for row, col, color in zip(rows, cols, colors):
      if color == 4:
        length = 1
        while True:
          good = True
          for r in range(row - length, row + length + 1):
            for c in range(col - length, col + length + 1):
              if common.get_pixel(grid, r, c) == 5:
                good = False
          if not good:
            length -= 1
            break
          length += 1
          if length >= width or length >= height: return None, None  # Too big.
        if length == 0: return None, None  # Too small.
        for r in range(row - length, row + length + 1):
          for c in range(col - length, col + length + 1):
            if common.get_pixel(output, r, c) != 0: return None, None
            output[r][c] = 2
    for row, col, color in zip(rows, cols, colors):
      if color == 4: output[row][col] = grid[row][col] = color
    return grid, output

  if width is None:
    width, height = common.randint(7, 30), common.randint(7, 30)
    while True:
      pixels = common.random_pixels(width, height, 0.025)
      if not pixels: continue
      rows, cols = zip(*pixels)
      colors = [4 if common.randint(0, 2) == 0 else 5 for _ in range(len(rows))]
      if len(set(colors)) == 1: continue
      grid, _ = draw()
      if grid: break

  grid, output = draw()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=8, height=9, rows=[1, 3], cols=[2, 3], colors=[5, 4]),
      generate(width=10, height=9, rows=[3, 3], cols=[1, 4], colors=[5, 4]),
      generate(width=11, height=9, rows=[1, 5], cols=[5, 4], colors=[5, 4]),
      generate(width=10, height=12, rows=[0, 2, 3, 4, 5, 7, 8, 10, 11],
               cols=[6, 3, 8, 1, 4, 0, 6, 1, 9],
               colors=[5, 4, 5, 5, 5, 5, 4, 5, 5]),
  ]
  test = [
      generate(width=20, height=30,
               rows=[2, 5, 7, 11, 15, 15, 16, 19, 19, 19, 25, 27, 27],
               cols=[15, 6, 14, 3, 10, 15, 18, 1, 8, 14, 5, 1, 15],
               colors=[5, 4, 5, 5, 5, 4, 5, 5, 5, 5, 4, 5, 5]),
  ]
  return {"train": train, "test": test}
