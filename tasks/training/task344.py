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


def generate(width=None, height=None, rows=None, cols=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the input grid
    height: the height of the input grid
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    colors: a list of digits representing the colors to be used
  """
  if width is None:
    width, height = common.randint(3, 10), common.randint(3, 10)
    bitmap = common.grid(width, height)
    # Draw random gray cells
    for pixel in common.random_pixels(width, height, 0.04):
      bitmap[pixel[0]][pixel[1]] = common.gray()
    # Choose sufficiently-spaced random red cells
    rows, cols = [], []
    for pixel in common.random_pixels(width + 2, height + 2, 0.08):
      r, c = pixel[0] - 1, pixel[1] - 1
      overlaps = False
      for row, col in zip(rows, cols):
        if abs(row - r) + abs(col - c) > 2: continue
        overlaps = True
      if overlaps: continue
      rows.append(r)
      cols.append(c)
      common.draw(bitmap, r, c, common.red())
      if not common.randint(0, 3): continue  # Rarely, we don't add a green cell
      if common.randint(0, 1):
        common.draw(bitmap, r, c + common.choice([-1, 1]), common.green())
      else:
        common.draw(bitmap, r + common.choice([-1, 1]), c, common.green())
    # Extract pixels from the bitmap.
    rows, cols, colors = [], [], []
    for r in range(height):
      for c in range(width):
        if not bitmap[r][c]: continue
        rows.append(r)
        cols.append(c)
        colors.append(bitmap[r][c])

  grid, output = common.grids(width, height)
  for r, c, color in zip(rows, cols, colors):
    output[r][c] = grid[r][c] = color
  for r, c, color in zip(rows, cols, colors):
    if color != common.green(): continue
    for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
      if common.get_pixel(output, r + dr, c + dc) != common.red(): continue
      output[r + dr][c + dc] = common.black()
      output[r][c] = common.cyan()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=3, height=3, rows=[0, 0, 2], cols=[0, 1, 1],
               colors=[3, 2, 5]),
      generate(width=6, height=7, rows=[0, 1, 1, 3, 3, 4, 5, 5],
               cols=[0, 2, 3, 1, 5, 1, 0, 3], colors=[5, 3, 2, 3, 2, 2, 5, 3]),
      generate(width=7, height=7, rows=[0, 1, 1, 2, 2, 2, 4, 5, 5, 5, 6],
               cols=[5, 0, 6, 0, 2, 3, 5, 0, 1, 5, 3],
               colors=[2, 3, 3, 5, 2, 3, 2, 3, 2, 3, 5]),
  ]
  test = [
      generate(width=9, height=7,
               rows=[0, 0, 1, 1, 1, 2, 3, 3, 4, 4, 5, 6, 6, 6, 6],
               cols=[4, 8, 1, 6, 7, 1, 4, 8, 0, 3, 7, 0, 1, 5, 7],
               colors=[2, 5, 2, 3, 2, 3, 5, 2, 5, 2, 3, 5, 3, 5, 2]),
  ]
  return {"train": train, "test": test}
