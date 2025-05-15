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
    width: the width of the grid
    height: the height of the grid
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    colors: a list of digits representing the colors to be used
  """
  if width is None:
    width, height = common.randint(15, 18), common.randint(15, 18)
    bitmap = common.grid(width, height)
    # First, add the static
    pixels = common.remove_neighbors(common.random_pixels(width, height, 0.05))
    for r, c in pixels:
      bitmap[r][c] = common.red()
    # Second, add the olives
    for r1, c1 in common.random_pixels(width, height, 0.02):
      vert = common.randint(0, 1)
      r2, c2 = r1 + vert, c1 + 1 - vert
      if r2 == height or c2 == width: continue
      # Check for overlap with other olives
      overlaps = False
      for r, c in [(r1, c1), (r2, c2)]:
        for dr in [-1, 0, 1]:
          for dc in [-1, 0, 1]:
            if common.get_pixel(bitmap, r + dr, c + dc) == common.green():
              overlaps = True
      if overlaps: continue
      # Draw the olives
      for r, c in [(r1, c1), (r2, c2)]:
        for dr in [-1, 0, 1]:
          for dc in [-1, 0, 1]:
            common.draw(bitmap, r + dr, c + dc, common.green())
      bitmap[r1][c1] = bitmap[r2][c2] = common.red()
    rows, cols, colors = [], [], []
    for r in range(height):
      for c in range(width):
        if not bitmap[r][c]: continue
        rows.append(r)
        cols.append(c)
        colors.append(bitmap[r][c])

  grid, output = common.grids(width, height)
  for r, c, color in zip(rows, cols, colors):
    grid[r][c] = color if color != common.green() else common.black()
    output[r][c] = color
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=18, height=15,
               rows=[1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 4, 4, 4, 4, 8, 11, 11, 12,
                     14, 14],
               cols=[6, 7, 8, 2, 6, 7, 8, 6, 7, 8, 6, 7, 8, 13, 17, 4, 8, 0, 0,
                     17],
               colors=[3, 3, 3, 2, 3, 2, 3, 3, 2, 3, 3, 3, 3, 2, 2, 2, 2, 2, 2,
                       2]),
      generate(width=16, height=15,
               rows=[0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 3, 3,
                     3, 4, 4, 4, 4, 4, 5, 5, 6, 6, 6, 7, 12, 13, 14, 14],
               cols=[7, 8, 9, 10, 12, 13, 14, 0, 7, 8, 9, 10, 12, 13, 14, 12,
                     13, 14, 8, 14, 15, 2, 10, 13, 14, 15, 14, 15, 10, 14, 15,
                     1, 1, 14, 2, 10],
               colors=[3, 2, 2, 3, 3, 2, 3, 2, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 2,
                       3, 3, 2, 2, 2, 3, 2, 3, 2, 2, 3, 3, 2, 2, 2, 2, 2]),
  ]
  test = [
      generate(width=16, height=17,
               rows=[0, 1, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 5, 6, 6, 6,
                     6, 7, 7, 7, 7, 7, 7, 7, 8, 8, 8, 8, 8, 8, 8, 9, 9, 9, 9,
                     10, 10, 10, 10, 10, 10, 10, 10, 11, 11, 11, 11, 12, 12, 12,
                     12, 12, 12, 12, 12, 13, 13, 13, 13, 13, 13, 13, 13, 13, 14,
                     14, 14, 14, 14, 14, 15, 16],
               cols=[15, 4, 7, 8, 9, 10, 13, 15, 7, 8, 9, 10, 7, 8, 9, 10, 12,
                     1, 2, 3, 4, 1, 2, 3, 4, 13, 14, 15, 1, 2, 3, 4, 13, 14, 15,
                     6, 13, 14, 15, 0, 7, 8, 9, 10, 13, 14, 15, 8, 9, 10, 11, 2,
                     4, 5, 6, 7, 8, 9, 10, 1, 5, 6, 7, 8, 9, 10, 11, 13, 3, 5,
                     6, 7, 8, 15, 7, 8],
               colors=[2, 2, 3, 3, 3, 3, 2, 2, 3, 2, 2, 3, 3, 3, 3, 3, 2, 3, 3,
                       3, 3, 3, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 3, 2, 3, 2,
                       3, 2, 2, 3, 3, 3, 3, 3, 3, 3, 2, 3, 2, 2, 2, 3, 3, 3, 3,
                       2, 3, 2, 3, 2, 2, 3, 3, 3, 2, 2, 2, 3, 3, 3, 3, 2, 2,
                       2]),
  ]
  return {"train": train, "test": test}
